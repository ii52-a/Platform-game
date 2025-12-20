import random

import pygame

import message
import rules
from Config import Screen

rule = rules.Rule()


class Platform:
    def __init__(self, x=Screen.ScreenX, y=None, width=220, height=25, color=(100, 100, 100)):
        self.rule = rules.Rule()
        self.y = random.randint(100, 300) if y is None else y
        self.x = x
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.color = color
        self.speed_x = 2.5 + self.rule.stage * 0.5  # 平台移动速度
        self.speed_y = 1
        self.is_active = True  # 平台是否可用
        self.width = width
        self.height = height
        self.if_player = False
        self.message = message.Message()
        self.last_pos = [self.rect.x, self.rect.y]

    def update(self):
        if self.is_active:
            self.rect.x -= self.speed_x
            self.rect.y += self.speed_y
        if self.rect.x < 0 - self.width or self.rect.y > Screen.ScreenY + self.height:
            self.is_active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)


class PlatformsManager:
    def __init__(self):
        self.platforms = []
        self.spawn_counter = 0
        self.rules = rules.Rule()

    def update(self, spawn_interval):
        self.spawn_counter += 1  # 每帧增加
        # 显示当前计数器和间隔

        if self.spawn_counter >= spawn_interval:
            self.spawn_create_SIPplatform()
            if random.random() < 0.05 + 0.05 * self.rules.stage:
                self.spawn_create_platform()

            self.spawn_counter = 0  # 重置计数器
        for p in self.platforms:
            if not p.is_active:
                self.platforms.remove(p)
                del p
        for platform in self.platforms:
            platform.update()

    def spawn_create_SIPplatform(self):
        self.platforms.append(self.rules.sample_platform_create_rule(
            [SIPHighPlatform, PlatformKSP, Platform,SpFragilePlatform]
        ))

    def spawn_create_platform(self):
        self.platforms.append(self.rules.platform_create_rule([
            SpUpPlatform, SpDownPlatform, SpFragilePlatform,
        ]))

    def boss_exPlatform(self):
                self.platforms.append(self.rules.platform_boss_rule([
                    SIPrightMovePlatform,SPrightFrpPlatform
                ]))

    def draw_all_platforms(self, screen):
        for platform in self.platforms:
            platform.draw(screen)

    def check_collision(self, player_rect):
        for platform in self.platforms:
            if platform.check_collision(player_rect):
                return platform
        return None


#初始平台
class PlatformFirst(Platform):
    def __init__(self, player_pos, width=250, height=30, color=(0, 75, 0)):
        # 计算平台位置：玩家脚下
        x = player_pos[0] - width // 2  # 玩家位置居中
        y = player_pos[1] + 20  # 玩家半径下方
        self.pos = (x, y)
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        # 初始不移动
        self.speed_x = 0
        self.speed_y = 0
        self.is_gaming = False

    def update(self):
        # print(self.is_gaming)
        if self.is_gaming:
            self.speed_x = 1
            self.speed_y = 1
        super().update()


"""定速块"""


class PlatformKSP(Platform):  #定速定时块
    def __init__(self):
        super().__init__(height=random.randint(30, 25 + 7 * rules.Rule.stage))
        self.speed_x = 3 + 0.1 * rules.Rule.stage
        self.speed_y = 1.2


"""胖块"""


class SIPHighPlatform(Platform):
    def __init__(self):
        super().__init__(height=random.randint(30, 25 + 10 * rules.Rule.stage))


"""易碎平台"""


class SpFragilePlatform(Platform):
    def __init__(self):
        super().__init__()
        self.is_player = None
        self.destroy_time = 120 - self.rule.stage * 10  ###
        self.destroy_counter = 0
        self.destroy_now = False

    def update(self):
        super().update()
        if self.if_player and not self.destroy_now:
            self.color = (222, 233, 26)
            self.destroy_now = True
        if self.destroy_counter > self.destroy_time / 2:
            self.color = (207, 74, 74)
        if self.destroy_now:
            self.self_destroy()

    def self_destroy(self):
        self.destroy_counter += 1
        # print(self.destroy_counter)
        if self.destroy_counter > self.destroy_time:
            self.is_player = None
            self.is_active = False

    def draw(self, screen):
        super().draw(screen)
        if self.destroy_now:
            self.message.font_draw("", f"{self.destroy_time - self.destroy_counter}", screen,
                                   self.rect.x + self.width + 5, self.rect.y - 10, self.color)


"""上升平台"""


class SpUpPlatform(Platform):
    def __init__(self):

        super().__init__(color=(25, 60, 80))

    def update(self):
        add_x = self.speed_x
        add_y = self.speed_y
        if self.is_active:
            if self.if_player:
                self.speed_x += -0.5 - 0.2 * self.rule.stage
                self.speed_y += -0.2 - self.rule.stage * 0.5
            self.rect.x -= self.speed_x
            self.rect.y += self.speed_y
        self.speed_x = add_x
        self.speed_y = add_y
        if self.rect.x < 0 - self.width or self.rect.y > 720 + self.height:
            self.is_active = False

    def draw(self, screen):
        super().draw(screen)
        self.message.font_draw("", "UP", screen, self.rect.x + self.width + 5, self.rect.y - 10, (225, 45, 3))


"""下降平台"""


class SpDownPlatform(Platform):
    def __init__(self):
        self.y = random.randint(400, 550 + rule.stage * 25)
        super().__init__(y=self.y, color=(25, 60, 80))
        self.speed_y = -1

    def update(self):
        add_x = self.speed_x
        add_y = self.speed_y
        if self.is_active:
            if self.if_player:
                self.speed_x += -0.5 - 0.2 * self.rule.stage
                self.speed_y += 0.5 + self.rule.stage * 0.5
            self.rect.x -= self.speed_x
            self.rect.y += self.speed_y
        self.speed_x = add_x
        self.speed_y = add_y
        if self.rect.x < 0 - self.width or self.rect.y > 720 + self.height:
            self.is_active = False

    def draw(self, screen):
        super().draw(screen)
        self.message.font_draw("", "DOWN", screen, self.rect.x + self.width + 5, self.rect.y - 10, (225, 45, 3))


"""简单平台"""
class SIPrightMovePlatform(Platform):
    def __init__(self):
        self.x=0
        self.y=random.randint(50, 150)
        super().__init__(x=self.x,y=self.y)
        self.speed_x = 2
        self.speed_y = 1

    def update(self):
        if self.is_active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        if self.rect.x > Screen.ScreenX or self.rect.y > Screen.ScreenY + self.height:
            self.is_active = False

class SPrightFrpPlatform(SpFragilePlatform):
    def __init__(self):
        super().__init__()
        self.rect.x=0
        self.rect.y=random.randint(50, 150)
        self.speed_x = 2
        self.speed_y = 1
    
    def update(self):
        super().update()
        if self.is_active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        if self.rect.x > Screen.ScreenX or self.rect.y > Screen.ScreenY + self.height:
            self.is_active = False
        

