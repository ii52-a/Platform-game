import random

import pygame

from loop import rules
from loop.Config import Screen
from EffectGlobal import Global
from Enemy.Basic_Enemy import BasicEnemy
from Effects import *


class IceEnemy(BasicEnemy):
    """
    冰怪物：
        技能：锁定平台一段时间后使其破碎，每次使用技能扣除10点生命
        特性：被玩家碰撞立刻死亡，同时生成
    """
    def __init__(self, screen, player, traps, platform,enemy, width=50, height=50,if_name=True, radius=None):
        y=random.randint(80,Screen.ScreenY//2)
        super().__init__(screen, player, traps, platform,y=y,width=width, height=height, radius=radius,
                 color=(5, 13, 119),enemy=None)
        self.health= 30 + rules.Rule.stage * 5
        self.locked_platform = None  # 被锁定的平台
        self.lock_radius = 20  # 圆环的半径
        self.damage_time=220
        self.once_locked=True
        self.effect=[]
        self.name='冰寒'
        self.if_name=if_name
        self.boss=None

    def draw(self,if_hp=False,name=None):
        if self.locked_platform:
            pygame.draw.line(self.screen,(23, 178, 255),start_pos=(self.rect.x,self.rect.y), end_pos=(self.locked_platform.rect.centerx,self.locked_platform.rect.centery))
        super().draw(if_hp=if_hp,name=self.name if self.if_name else None)



    def update(self):
        self.damage_counter += 1
        if self.health <= 0:
            self.effect.append(CycleDeath(self.rect.centerx, self.rect.centery))
            self.is_alive = False
            if self.boss:
                self.boss.link_self_damage()
        if self.damage_counter >= 120 and self.once_locked:
           self.lock_break_platform()
           self.once_locked=False

           self.radius += 5

        elif self.damage_counter >= self.damage_time:
            self.break_platform()
            self.once_locked=True
            self.damage_counter = 0
            self.radius-=5
        self.apply_damage()

    def apply_damage(self):
        if self.check_circle_collision(self.rect,self.radius,self.player.pos,self.player.radius):
            self.health =0
            self.locked_platform = None
            Global.shark_time=8


    def lock_break_platform(self):
        self.color =(81, 91, 235)
        mint=max(0,len(self.platform.platforms)-2)
        while self.locked_platform is None or self.locked_platform.no_break:
            self.locked_platform=self.platform.platforms[random.randint(mint,len(self.platform.platforms)-1)]
        self.locked_platform.color=(87, 199, 255)



    def break_platform(self):
        if self.locked_platform:
            self.platform.effects.append(CycleDeath(self.locked_platform.rect.centerx, self.locked_platform.rect.centery))
            self.locked_platform.is_active=False
            self.locked_platform=None


        self.health-=10
        self.color=(5, 13, 119)
