import threading

import pygame

from loop import rules
from EffectGlobal import Global
from Effects import BossDeathEffect
from Trap import *
from loop.Config import Config
from Enemy import Enemy


class BlackHole(Enemy):
    """
    第一boss-黑洞
        使用光环扩散，触碰到玩家将发射激光，伤害2
    """
    def __init__(self, screen, player, traps, platform,enemy):
        super().__init__(screen=screen, player=player, traps=traps, platform=platform,enemy=enemy)
        self.health = Config.FIRST_BOSS_HEALTH
        self.radius = 50
        self.rect.x = 640
        self.rect.y = 120
        self.damage_counter = 180
        self.damage_time =Config.FIRST_BOSS_INTERNAL
        self.if_tx = False
        self.tx_radius = self.radius
        self.create_platform_counter=0
        self.create_platform_cycle=130


    def update(self):
        rules.Rule.if_boss = True
        rules.Rule.boss_stage = 1
        self.damage_counter += 1
        if self.damage_counter >= self.damage_time:
            self.health -= 30
            self.call_laser()
            self.damage_counter = 0
        if self.health <= 0:
            self.effect.append(BossDeathEffect(self.rect.centerx, self.rect.centery))
            self.is_alive = False
            rules.Rule.if_boss = False
        self.platform_create()


    def create_cycle(self):
        a=pygame.draw.circle(self.screen, (255, 37, 37), (self.rect.x, self.rect.y), radius=self.tx_radius, width=5)
        self.tx_radius += 6

        if self.check_circle_collision((self.rect.x, self.rect.y), self.tx_radius,self.player.pos,self.player.radius):
            self.trapManager.advance_create(
                LockLaser(screen=self.screen, player=self.player,damage=2, if_advance_time=False))
        if self.tx_radius >= 220+(250-self.health):
            self.if_tx = False
            self.tx_radius = self.radius

    def draw(self):
        if self.if_tx:
            self.create_cycle()
        super().draw()


    def call_laser(self):
        fcolor = self.color
        self.color = (255, 37, 37)
        radius_c = self.radius
        self.radius = 60
        self.if_tx = True
        Global.shark_time=6

        def l():
            self.radius = radius_c
            self.color = fcolor
            if self.color !=self.init_color:
                self.color = self.init_color

        threading.Timer(0.5, l).start()
        self.trapManager.advance_create(Laser(screen=self.screen, player=self.player))

    def platform_create(self):
        self.create_platform_counter+=1
        if self.create_platform_counter > self.create_platform_cycle:
            self.platform.boss_exPlatform()
            self.create_platform_counter = 0
            self.trapManager.advance_create(Laser(screen=self.screen, player=self.player))



    def __del__(self):

        for _ in range(3):
            self.trapManager.advance_create(Laser(screen=self.screen, player=self.player, if_advance_time=False))
        for _ in range(10):
            self.trapManager.advance_create(
                LockLaser(screen=self.screen, player=self.player, if_advance_time=False))