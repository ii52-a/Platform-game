import random
import threading

import pygame
import message
import trap
import rules
from Config import Screen, Config


class Enemy:
    def __init__(self, screen, player, traps, platform, x=None, y=None, width=50, height=50, radius=None,
                 color=(0, 0, 0)):
        x = random.randint(0, Screen.ScreenX - 1) if x is None else x
        y = random.randint(0, 720 - 1) if y is None else y
        self.radius = 20 if radius is None else radius

        self.health = 100
        self.damage = 10

        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 10

        self.screen = screen
        self.player = player
        self.init_color=color
        self.color = self.init_color

        self.message = message.Message()

        self.is_alive = True
        self.damage_time = 400
        self.damage_counter = 0
        self.trapManager = traps
        self.platform = platform



    def move(self):
        pass

    def update(self):
        pass

    def draw(self):
        w = self.radius if self.radius is not None else self.rect.width

        self.message.font_draw("HP", f"{self.health:.1f}", self.screen, self.rect.x + w, self.rect.y + 5, self.color)
        if self.radius is not None:
            pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y), radius=self.radius)
        else:
            pygame.draw.rect(self.screen, self.color, (self.rect.x, self.rect.y))

    def apply_damage(self):
        pass









