import math
import random

import pygame

from Effects.LineEffect import LightningEffect
from Manager.PlatFormGenerator import SimpleGenerator
from Manager.PlatFormGenerator.Boss_Blackhole_Pgenerator import BlackHoleGenerator
from loop import rules
from EffectGlobal import Global
from Effects import BossDeathEffect
from Trap import *
from loop.Config import Config, Screen
from Enemy import Enemy, BlackEnemy


class MirageBound(Enemy):
    """
    最终boss-迷惘 第一阶段:覆灭者 ParadoxEidolon

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

        #玩家动量
        self.player_dx=0
        self.player_dy=0





        #启用特殊阶段平台生成
        self.use_sp_platform_generator(BlackHoleGenerator)


    def update(self):
        rules.Rule.if_boss = True
        rules.Rule.boss_stage = 3
        pass



