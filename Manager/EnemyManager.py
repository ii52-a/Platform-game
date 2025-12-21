import rules
from Enemy import *


class EnemyManager:
    def __init__(self, player, screen, traps, platform):
        self.enemies = []
        self.effects=[]
        self.player = player
        self.create_counter = 0
        self.screen = screen
        self.enemy_counter = 0
        self.rules = rules.Rule()
        self.FirstBoss = True
        self.trapManager = traps
        self.platform = platform

    def update(self, time=500):
        if time != -1:
            self.enemy_counter += 1
            if self.enemy_counter >= time:
                self.enemies.append((rules.Rule.create_enemy(
                    [IceEnemy]
                ))(self.screen,self.player,self.trapManager,self.platform))
                self.enemy_counter =0
        if self.rules.get_stage() == 5 and self.FirstBoss:
            self.rules.boss_stage = 1
            self.FirstBoss = False
            self.create_enemy(BossStageFirst(self.screen, self.player, self.trapManager, self.platform))

            rules.Rule.if_boss = True
        for p in self.enemies[:]:
            if not p.is_alive:
                self.effects.append(p.effect)
                self.enemies.remove(p)
                del p
            else:
                p.update()

        for e in self.effects[:]:
            e.update()
            if not e.is_alive:
                self.effects.remove(e)
    def draw(self):
        for i in self.enemies:
            i.draw()
        for e in self.effects:
            e.draw(self.screen)

    def create_enemy(self, ad):
        self.enemies.append(ad)

    def check_collision(self, player_rect):
        for i in self.enemies:
            if i.rect.colliderect(player_rect):
                i.apply_damage()
