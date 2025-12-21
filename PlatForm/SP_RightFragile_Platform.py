"""右移易碎平台"""
import random

from Config import Screen
from PlatForm import SpFragilePlatform



class SPrightFrpPlatform(SpFragilePlatform):
    def __init__(self):
        super().__init__()
        self.rect.x = 0
        self.rect.y = random.randint(50, 150)
        self.speed_x = 2
        self.speed_y = 1

    def update(self):
        super().update()
        if self.is_active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        if self.rect.x > Screen.ScreenX or self.rect.y > Screen.ScreenY + self.height:
            self.is_active = False

