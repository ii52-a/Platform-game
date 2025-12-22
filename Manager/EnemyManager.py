from loop import rules
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
        self.Boss = [True,True]
        self.trapManager = traps
        self.platform = platform

    def update(self):
        self.enemy_counter += 1
        if self.enemy_counter >= self.rules.create_enemy_time() and len(self.enemies)<=5:
            self.enemies.append((rules.Rule.create_enemy(
                [TreatEnemy,BlackEnemy,IceEnemy]
            ))(self.screen,self.player,self.trapManager,self.platform,self))
            self.enemy_counter =0
        print(self.rules.get_stage(), self.Boss)
        if self.rules.get_stage() == 5 and self.Boss[0]:
            self.rules.boss_stage = 1
            self.Boss[0] = False
            self.create_enemy(BlackHole(self.screen, self.player, self.trapManager, self.platform,self))

        elif self.rules.get_stage() == 8 and self.Boss[1]:
            rules.Rule.if_boss = True
            self.Boss[1] = False
            self.create_enemy(IceBlue(self.screen, self.player, self.trapManager, self.platform,self))
        for p in self.enemies[:]:
            if not p.is_alive:
                if p.effect:
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
