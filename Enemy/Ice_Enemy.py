import random

import pygame

import rules
from Config import Screen
from Enemy.Enemy import Enemy
from effects import IceDeath


class IceEnemy(Enemy):
    """
    冰怪物：
        技能：锁定平台一段时间后使其破碎，每次使用技能扣除10点生命
        特性：被玩家碰撞立刻死亡，同时生成
    """
    def __init__(self, screen, player, traps, platform, width=50, height=50, radius=None):
        y=random.randint(80,Screen.ScreenY//2)
        super().__init__(screen, player, traps, platform,y=y,width=width, height=height, radius=radius,
                 color=(5, 13, 119))
        self.health=30 + rules.Rule.stage*10
        self.locked_platform = None  # 被锁定的平台
        self.lock_radius = 20  # 圆环的半径
        self.damage_time=240
        self.once_locked=True
        self.effect=None

    def draw(self):
        if self.locked_platform:
            pygame.draw.circle(self.screen, (23, 178, 255),
                               (self.locked_platform.rect.centerx, self.locked_platform.rect.centery), self.lock_radius,
                               3)
            pygame.draw.line(self.screen,(23, 178, 255),start_pos=(self.rect.x,self.rect.y), end_pos=(self.locked_platform.rect.centerx,self.locked_platform.rect.centery))
        super().draw()



    def update(self):
        self.damage_counter += 1
        if self.health <= 0:
            self.effect=IceDeath(self.rect.centerx, self.rect.centery)
            self.is_alive = False
        if self.damage_counter >= 180 and self.once_locked:
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
        if self.rect.colliderect(self.player.get_rect()):
            self.health =0


    def lock_break_platform(self):
        self.color =(81, 91, 235)
        self.locked_platform=self.platform.platforms[random.randint(0,len(self.platform.platforms)-1)]
        self.locked_platform.color=(87, 199, 255)



    def break_platform(self):
        if self.locked_platform:
            self.platform.effects.append(IceDeath(self.locked_platform.rect.centerx, self.locked_platform.rect.centery))
            self.locked_platform.is_active=False
            self.locked_platform=None


        self.health-=10
        self.color=(5, 13, 119)
