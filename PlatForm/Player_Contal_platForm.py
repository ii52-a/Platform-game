"""平台位置依靠玩家移动"""

import random

import pygame

from loop import rules, message
from loop.Config import Screen

#初始平台
from PlatForm.platform import Platform


class PlatformControl(Platform):
    def __init__(self, player, width=250, height=30, color=(0, 75, 0)):
        # 平台位置：玩家脚下
        x = player.get_rect().x - width // 2  # 玩家位置居中
        y = player.get_rect().y + 20  # 玩家半径下方
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        # 不移动
        self.tplayer = player
        self.speed_x = 0
        self.speed_y = 0
        self.is_gaming = False

    def update(self):
        # print(self.is_gaming)
        player_rect = self.tplayer.get_rect()
        self.rect.centerx = player_rect.centerx
        self.rect.top = player_rect.bottom

        #归零修正
        self.last_pos = [self.rect.x, self.rect.y]

    def debind_player(self):
        pass