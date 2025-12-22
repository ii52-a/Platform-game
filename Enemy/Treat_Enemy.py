import random



from loop.Config import Screen
from Enemy import Enemy
from Effects import *


class TreatEnemy(Enemy):
    def __init__(self, screen, player, traps,enemy, platform, width=50, height=50, radius=None):
        y=random.randint(80,Screen.ScreenY//2)
        super().__init__(screen, player, traps, platform,y=y,width=width, height=height, radius=radius,
                 color=(79, 221, 60),enemy=None)
        self.health=300
        self.effect=None
        self.once=True

    def draw(self):
        self.message.font_draw("Friend", "", self.screen, self.rect.centerx - self.radius * 2,
                               self.rect.y - self.radius - 12, self.color, font_size=16)
        super().draw()



    def update(self):
        self.health -=1
        if self.health <= 0:
            self.is_alive = False

        self.apply_damage()

    def apply_damage(self):
        if self.rect.colliderect(self.player.get_rect()):
            self.health =0
            if self.once:
                self.player.health += 10
                self.effect = TreatDeath(self.player.pos[0], self.player.pos[1], self.color)
                self.once=False