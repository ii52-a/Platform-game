import math

import pygame

from Effects import SlashEffect
from Manager.PlatFormGenerator import Generator
from loop.Config import Screen
from PlatForm import *

class NexusGenerator(Generator):
    def __init__(self,platforms,rules):
        super().__init__(platforms,rules)
        self.once=True
        self.effects=[]

    def update(self):

        if self.once:
            self.once=False
            self._init_nexus()

    def generator_create_platform(self):
        pass

    def generator_create_SIPplatform(self):
        pass

    def _init_nexus(self):
        for i in self.platforms:
            i.is_active=False
            self.platformManager.effects.append(SlashEffect(i.rect.x,i.rect.y,(0,0,0)))
        self.platforms.append(Platform(x=0,y=Screen.ScreenY-50,speed_y=0,speed_x=0,width=Screen.ScreenX,no_dump=True))
        width=200   #总宽
        count = 5  #奇数个
        mid_x=Screen.ScreenX//2 -width//2  #中心点
        x_interval=Screen.ScreenX/(count+1)
        y_interval=(Screen.ScreenY-50)/ (count+1)
        x_init=200
        y_init=Screen.ScreenY-50-y_interval

        self.platforms.append(Platform(x=mid_x, y=y_init, speed_x=0, speed_y=0, width=width))
        y_init -= y_interval
        for i in range(count//2):
            self.platforms.append(Platform(x=mid_x - x_init, y=y_init, speed_x=0, speed_y=0, width=width))
            self.platforms.append(Platform(x=mid_x + x_init, y=y_init, speed_x=0, speed_y=0, width=width))
            x_init += x_interval
            y_init -= y_interval
        x_init -= x_interval *2
        for i in range(count//2-1):
            self.platforms.append(Platform(x=mid_x - x_init, y=y_init, speed_x=0, speed_y=0, width=width))
            self.platforms.append(Platform(x=mid_x + x_init, y=y_init, speed_x=0, speed_y=0, width=width))
            x_init -= x_interval
            y_init -= y_interval
        self.platforms.append(Platform(x=mid_x, y=y_init, speed_x=0, speed_y=0, width=width))


    def __str__(self):
        return "Nexus圣所"