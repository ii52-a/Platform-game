from loop import rules
from EffectGlobal import Global

from Enemy import Enemy
from Trap import *
from Effects import *


class BlackEnemy(Enemy):
    def __init__(self, screen, player, traps, platform,enemy, width=50, height=50, radius=30):
        super().__init__(screen, player, traps, platform, width=width, height=height, radius=radius,
                         color=(45, 45, 45),enemy=enemy)
        self.health = 40 + rules.Rule.stage * 5
        self.damage_time = 200
        self.once_locked = True
        self.effect = None
        self.lack=None

    def draw(self):
        super().draw()

    def update(self):
        self.damage_counter += 1
        if self.health <= 0 or self.radius <=6:
            self.is_alive = False
            # self.effect = IceDeath(self.rect.centerx, self.rect.centery,(91, 91, 91),110,3,8)
            self.effect=SlashEffect(self.rect.centerx, self.rect.centery, self.color)

        if self.damage_counter >= self.damage_time:
            self.damage_counter = 0
            self.radius -= 3
            self.health -= 10
            self.lack = LockLaser(screen=self.screen, player=self.player
                                                            ,color=(110, 110, 110),advance_timer=250,
                                                            damage=5,advance_color=(91, 91, 91))
            self.trapManager.advance_tarps.append(self.lack)
        self.apply_damage()

    def apply_damage(self):
        if self.rect.colliderect(self.player.get_rect()):
            self.health = 0
            Global.shark_time=10
