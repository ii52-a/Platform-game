import random

import pygame

import rules
from Config import Screen
from message import Message


class Trap:
    """陷阱基类，所有陷阱的父类"""
    screen_pos_width = 1280
    screen_pos_height = 720

    def __init__(self, player, screen, x=None, y=0, width=20, height=Screen.ScreenY, damage=10, color=(128, 128, 128),
                 speed_x=0, speed_y=0, ):
        self.x = random.randint(0, self.screen_pos_width) if x is None else x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)

        self.rule = rules.Rule()

        self.speed_x = speed_x
        self.speed_y = speed_y
        self.damage = damage  # 陷阱造成的伤害

        self.color = color
        self.player = player
        self.message = Message()

        """生命周期"""

        self.life_time = 0
        self.life_cycle = 120
        self.is_active = True  # 是否激活

        """伤害周期"""
        self.damage_cycle = 40
        self.damage_time = self.damage_cycle

        """提前渲染信息"""
        self.screen = screen
        self.advance_Timer = 60

    def update(self):
        """更新"""
        pass

    def draw(self, screen):
        """绘制"""
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, player_rect):
        return self.is_active and self.rect.colliderect(player_rect)

    def apply_damage(self):
        pass


class TarpManager:
    def __init__(self, player, screen):
        self.tarps = []
        self.player = player
        self.create_counter = 0
        self.screen = screen
        self.advance_tarps = []
        self.rule = rules.Rule()

    def update(self):
        for p in self.tarps:
            if not p.is_active or p.life_time > p.life_cycle:
                self.tarps.remove(p)
                del p
            else:
                p.life_time += 1

        for platform in self.tarps:
            platform.update()
        self.check_collision(self.player.get_rect())

    def auto_create_tarp(self, time):
        self.create_counter += 1
        if self.create_counter > time:
            for _ in range(self.rule.trap_lack_num()):
                self.advance_create()
            self.create_counter = 0
        for ad in self.advance_tarps:
            ad.advance_Timer -= 1
            if ad.advance_Timer == 0:
                self.advance_tarps.remove(ad)
                self.create_tarp(ad)

    def draw(self, screen):
        for platform in self.tarps:
            platform.draw(screen)
        for ad in self.advance_tarps:
            ad.advance_draw()

    def advance_create(self,ad=None):
        ad = self.rule.trap_create_rule([
            Laser, LockLaser, MoveLaser,RectXLaser
        ])(self.player, self.screen) if ad is None else ad
        if ad:
            ad.advance_draw()
            self.advance_tarps.append(ad)

    def create_tarp(self, ad):
        self.tarps.append(ad)

    def check_collision(self, player_rect):
        for tarp in self.tarps:
            if tarp.rect.colliderect(player_rect):
                tarp.apply_damage()


class Laser(Trap):
    def __init__(self, player, screen, x=None, y=0, width=20, height=Screen.ScreenY, damage=10, color=(128, 128, 128)):
        self.color = (214, 212, 71)
        super().__init__(player=player, color=self.color, screen=screen, width=width, height=height, damage=damage)
        self.life_cycle = 70 + 5 * self.rule.stage

    def advance_draw(self):
        self.message.font_draw('', f"{self.advance_Timer:.1f}", screen=self.screen, x=self.rect.x + self.rect.width,
                               y=10,
                               color=(210, 208, 120))
        pygame.draw.rect(self.screen, (255, 25, 25), (self.rect.x + self.rect.width / 2, 0, 2, self.screen_pos_height))

    def update(self):
        self.life_time += 1
        if self.damage_time < self.damage_cycle:
            self.damage_time += 1

        if self.life_time > self.life_cycle:
            self.is_active = False

    def draw(self, screen):
        self.message.font_draw('', f"{self.life_cycle - self.life_time:.1f}", screen=self.screen,
                               x=self.rect.x + self.rect.width + 5, y=10,
                               color=(41, 230, 255))

        super().draw(screen)

    def apply_damage(self):
        if self.damage_time >= self.damage_cycle:
            self.player.is_damaging(self.damage)
            self.damage_time = 0


class MoveLaser(Laser):
    def __init__(self, player, screen, speed_x=None):
        super().__init__(player, screen)
        self.speed_x = random.randint(-1 * self.rule.stage, 1 * self.rule.stage) if speed_x is None else speed_x

    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.right < 20:
            self.is_active = False
        elif self.rect.right > self.screen_pos_width-20:
            self.is_active = False
        super().update()

    def advance_draw(self):
        LorR = "Left" if self.speed_x < 0 else "Right"
        self.message.font_draw('', LorR, screen=self.screen,
                               x=self.rect.x - 35, y=10,
                               color=(160, 59, 163))
        super().advance_draw()


class LockLaser(Laser):
    def __init__(self, player, screen):
        super().__init__(player, screen)
        self.rect.x = max(min(random.randint(player.pos[0] - 250, player.pos[0] + 250),self.screen_pos_width-50),50)
        self.advance_speed_x = 0.8 + self.rule.stage * 0.3
        self.speed_x = 0
        self.life_cycle = 20 + 5 * self.rule.stage
        self.advance_Timer = 175
        self.damage = 10

    def advance_draw(self):
        if self.player.pos[0] > self.rect.x:
            self.rect.move_ip(min(self.advance_speed_x,2), 0)
        elif self.player.pos[0] < self.rect.x:
            self.rect.move_ip(max(-self.advance_speed_x,-2), 0)
        super().advance_draw()


class RectXLaser(Trap):
    def __init__(self, player, screen):

        y = random.randint(20, self.screen_pos_height - 20)

        super().__init__(
            player=player,
            screen=screen,
            x=0,
            y=y,
            width=self.screen_pos_width,
            height=20,
            damage=10,
            color=(214, 212, 71),
            speed_y=3
        )

        self.life_cycle = 75 + 5 * self.rule.stage
        self.damage_cycle = 45
        self.damage_time = self.damage_cycle

    def advance_draw(self):
        self.rect.move_ip(0,1)
        self.message.font_draw('', f"{self.advance_Timer:.1f}",
                               screen=self.screen,
                               x=self.screen_pos_width - 20,
                               y=self.rect.y + 20,
                               color=(210, 208, 120))

        # 绘制水平预警线
        pygame.draw.line(self.screen, (255, 25, 25),
                         (0, self.rect.centery),
                         (self.screen_pos_width, self.rect.centery),
                         2)

    def draw(self, screen):
        # 显示剩余时间
        self.message.font_draw('', f"{self.life_cycle - self.life_time:.1f}",
                               screen=self.screen,
                               x=self.screen_pos_width-20,  # 右上角显示
                               y=self.rect.y + 20,
                               color=(41, 230, 255))


        super().draw(screen)

    def update(self):
        self.life_time += 1
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.damage_time < self.damage_cycle:
            self.damage_time += 1

        if self.life_time > self.life_cycle:
            self.is_active = False

    def apply_damage(self):
        if self.damage_time >= self.damage_cycle:
            self.player.is_damaging(self.damage)
            self.damage_time = 0
