import random

import pygame

from loop import rules, message
from loop.Config import Screen

rule = rules.Rule()


class Platform:
    def __init__(self, x=Screen.ScreenX, y=None,width=220, height=25, color=(100, 100, 100)):
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
        self.player=None

    def bind_player(self,player):
        self.player=player

    def debind_player(self):
        self.if_player=False
        self.player=None

    def update(self):
        if not self.if_player:
            self.player=None
        if self.is_active:
            self.rect.x -= self.speed_x
            self.rect.y += self.speed_y
        if self.rect.x < 0 - self.width or self.rect.y > Screen.ScreenY + self.height:
            self.is_active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

