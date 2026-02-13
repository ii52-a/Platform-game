import math
import random

import pygame
from fontTools.designspaceLib.types import Rules

from EffectGlobal import Global
from Effects import CycleDeath
from Effects.CycleScreenShield import CycleScreenShield
from Effects.LineEffect import LightningEffect
from Enemy import BasicEnemy
from loop.Config import Screen
from loop.Event import Event
from loop.rules import Rule


class PortalFriend(BasicEnemy):
    def __init__(self,screen, player, traps, platform,enemy):
        super().__init__(screen, player, traps, platform,enemy)
        self.rect.x=Screen.ScreenX//2
        self.rect.y=Screen.ScreenY//2

        self.counter=-1


    def update(self):
        if self.check_circle_collision(self.rect,20,self.player.pos,self.player.radius):
            Global.shark_time=8

            if self.counter==-1:
                self.enemyManager.effects.append(
                    CycleScreenShield(self.rect.x, self.rect.y, (0, 0, 0), 800, 2)
                )
                self.counter=0
        if self.counter !=-1:
            dx=self.rect.x - self.player.pos[0]
            dy=self.rect.y - self.player.pos[1]
            d=math.sqrt(dx*dx+dy*dy)

            self.player.pos[0]=self.rect.x
            self.player.pos[1]=self.rect.y
            Global.shark_time = 6
            self.counter+=1
            # print(self.counter)
            if self.counter >=400:
                Event.score=30000
                self.is_alive=False


        else:
            dx = self.rect.x - self.player.pos[0]
            dy = self.rect.y - self.player.pos[1]
            d = math.sqrt(dx * dx + dy * dy)

            ddx = (dx / d) * 10
            ddy = (dy / d) * 50
            self.player.be_moved(ddx, ddy)



    def draw(self):
        for i in range(3):
            dy=(random.randint(Screen.ScreenX//2-50,Screen.ScreenX//2+50),random.randint(Screen.ScreenY//2-50,Screen.ScreenY//2+50))

            self.enemyManager.effects.append(
                LightningEffect((Screen.ScreenX // 2, Screen.ScreenY // 2), dy, color=(255,255,255)))

        if random.randint(0,1) >0.2:
            self.enemyManager.effects.append(
            CycleDeath(Screen.ScreenX // 2, Screen.ScreenY // 2, color=(0, 0, 0), speed=2, thickness=1))
            dy = (random.randint(50, Screen.ScreenX  - 50),
                  random.randint(50, Screen.ScreenY  - 50))
            self.enemyManager.effects.append(
                LightningEffect((Screen.ScreenX // 2, Screen.ScreenY // 2), dy, color=(255, 255, 255)))