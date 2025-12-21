"""易碎平台-冰形态"""
from PlatForm import SpFragilePlatform


class SPICEPlatform(SpFragilePlatform):
    def __init__(self,first_color=(108, 113, 253),second_color=(144, 146, 217)):
        super().__init__(first_color=first_color,second_color=second_color)
        self.color = (19, 24, 176)
        self.destroy_time = 100
        self.if_player_quik=False
        self.quik=15

    def update(self):
        super().update()
        if self.if_player and not self.if_player_quik:
            self.if_player_quik=True
            self.player.speed+=self.quik



    def self_destroy(self):
        super().self_destroy()
        if self.if_player_quik and self.if_player:
            self.player.speed-=self.quik
            self.if_player_quik=False

    def debind_player(self):
        if  self.if_player_quik:
            self.if_player_quik=False
            self.player.speed-=self.quik
        super().debind_player()