"""简单平台"""
import random

from loop.Config import Screen
from PlatForm.Basic_Platform import Platform


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
