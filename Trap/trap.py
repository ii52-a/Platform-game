import random

import pygame

from loop import rules
from loop.Config import Screen
from loop.message import Message


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





