import math
import random

import pygame

from Effects.LineEffect import LightningEffect
from Enemy.Basic_Enemy import BasicEnemy
from Manager.PlatFormGenerator import SimpleGenerator
from Manager.PlatFormGenerator.Boss_Blackhole_Pgenerator import BlackHoleGenerator
from loop import rules
from EffectGlobal import Global
from Effects import BossDeathEffect
from Trap import *
from loop.Config import Config, Screen
from Enemy import *


class BlackHole(BasicEnemy):
    """
    第一boss-黑洞
        使用光环扩散，触碰到玩家将发射激光，伤害2
    """
    def __init__(self, screen, player, traps, platform,enemy):
        super().__init__(screen=screen, player=player, traps=traps, platform=platform,enemy=enemy)
        self.radius_c = self.radius
        self.health = Config.FIRST_BOSS_HEALTH
        self.radius = 50
        self.rect.x = 640
        self.rect.y = 120
        self.damage_counter = 180
        self.damage_time =Config.FIRST_BOSS_INTERNAL

        #黑洞波圈激光内置cd / 计时器now
        self.call_laser_cd=60
        self.call_laser_now=0
        #抨击圈扩散
        self.if_back_pop=False
        #收缩
        self.if_back_pop_re=False
        self.black_pop_nradius= 20+self.radius
        self.black_pop_radius = 20+self.radius

        #玩家动量
        self.player_dx=0
        self.player_dy=0


        self.if_tx = False
        self.tx_radius = self.radius

        self.create_platform_counter=0
        self.create_platform_cycle=130

        self.fcolor=self.color
        self.colortk=0


        #启用特殊阶段平台生成
        self.use_sp_platform_generator(BlackHoleGenerator)
        rules.Rule.if_boss = True
        rules.Rule.boss_stage = 1


    def update(self):

        self.damage_counter += 1
        if self.damage_counter >= self.damage_time:
            self.health -= 30
            self.call_laser()

            self.damage_counter = 0
        if self.health <= 0:
            self.effect.append(BossDeathEffect(self.rect.centerx, self.rect.centery))
            self.is_alive = False
            self._death()
        now=pygame.time.get_ticks()
        self.black_pop()
        if now-self.colortk >=200 and self.color !=self.fcolor:
            self.radius = self.radius_c
            self.color = self.fcolor

    #红色扩散光圈
    def create_cycle(self):

        self.tx_radius +=2

        if self.check_circle_collision((self.rect.x, self.rect.y), self.tx_radius,self.player.pos,self.player.radius):
            dx = self.rect.x - self.player.pos[0]
            dy = self.rect.y - self.player.pos[1]
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist > 1:
                pull_strength = 8 +self.tx_radius//30
                tdx = (dx / dist) * pull_strength
                tdy = (dy / dist) * pull_strength
                self.player.be_moved(dx=tdx,dy=tdy)
            now=pygame.time.get_ticks()
            if  now-self.call_laser_now>=self.call_laser_cd:
                self.call_laser_now=now
                self.trapManager.advance_create(
                    LockLaser(screen=self.screen, player=self.player
                              , color=(110, 110, 110), advance_timer=200,
                              damage=2, advance_color=(91, 91, 91))
                )


        if self.tx_radius >= 220+(250-self.health):
            self.if_tx = False
            self.tx_radius = self.radius

    def draw(self):
        if self.if_tx:
            self.create_cycle()
            pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y), radius=self.tx_radius, width=5)
        self.black_pop_draw()
        super().draw()


    def call_laser(self):
        self.color = (255, 37, 37)
        self.radius_c = self.radius
        self.radius = 60
        self.if_tx = True
        Global.shark_time=6
        self.colortk=pygame.time.get_ticks()
        self.trapManager.advance_create(Laser(screen=self.screen, player=self.player))



    def black_pop(self):
        if self.check_circle_collision((self.rect.x, self.rect.y), self.black_pop_radius,self.player.pos,self.player.radius):
            if not self.if_back_pop and not self.if_back_pop_re:
                self.if_back_pop=True
            self.player_dx +=8+self.black_pop_radius/7
            self.player_dy +=8+self.black_pop_radius/7
        if abs(self.player_dx)>2 or abs(self.player_dy)>2:
            dx = (self.rect.x - self.player.pos[0])
            dy = (self.rect.y - self.player.pos[1])
            dist = math.sqrt(dx ** 2 + dy ** 2)
            tdx= -(dx/dist)*self.player_dx*0.75
            tdy= -(dy/dist)*self.player_dy*0.75
            self.player.be_moved(dx=tdx,dy=tdy)
            self.player_dx *=0.75
            self.player_dy *=0.75
        if self.if_back_pop:
            self.black_pop_radius *=1.03
            if self.black_pop_radius >=350:
                self.if_back_pop=False
                self.if_back_pop_re=True
        if self.if_back_pop_re:
            self.black_pop_radius /= 1.02
            if self.black_pop_radius <=self.black_pop_nradius:
                self.black_pop_radius = self.black_pop_nradius
                x=random.randint(50, Screen.ScreenX-50)
                y=random.randint(50, Screen.ScreenY-50)
                self.create_new_enemy(BlackEnemy, x=x,y=y,health=10)
                self.effect.append(LightningEffect(start_pos=(self.rect.x,self.rect.y),end_pos=(x,y),color=self.color))
                self.if_back_pop_re = False


    def black_pop_draw(self):
        draw_radius=self.black_pop_radius+(self.black_pop_radius-self.black_pop_nradius) //30
        pygame.draw.circle(self.screen,(255, 37, 37),(self.rect.x,self.rect.y),radius=draw_radius,width=2)


    def _death(self):
        for _ in range(3):
            self.trapManager.advance_create(Laser(screen=self.screen, player=self.player, if_advance_time=False))
        for _ in range(10):
            self.trapManager.advance_create(
                LockLaser(screen=self.screen, player=self.player, if_advance_time=False))
        self.use_sp_platform_generator(SimpleGenerator)
        rules.if_boss=False

    def __del__(self):
        rules.if_boss=False