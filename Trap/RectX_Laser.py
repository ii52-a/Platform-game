import random

import pygame

from Trap.trap import Trap


class RectXLaser(Trap):
    def check_collision(self, player_rect):
        super().check_collision(player_rect)

    def __init__(self, player, screen,if_advance_time=True,speed_y=3,):

        self.if_advance_time =if_advance_time
        y = random.randint(20, self.screen_pos_height - 20)
        self.advance_tick=0
        self.speed_y = speed_y


        super().__init__(
            player=player,
            screen=screen,
            x=0,
            y=y,
            width=self.screen_pos_width,
            height=20,
            damage=10,
            color=(214, 212, 71),
            speed_y=self.speed_y
        )

        self.life_cycle = 75 + 5 * self.rule.stage
        self.damage_cycle = 45
        self.damage_time = self.damage_cycle

    def advance_draw(self):
        self.rect.move_ip(0,1)
        if self.if_advance_time:
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