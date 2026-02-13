from Manager.TrapGenerator.Simple_Tgenerator import SimpleTgenerator
from loop import rules

class TarpManager:
    def __init__(self, player, screen):
        self.traps = []
        self.player = player
        self.create_counter = 0
        self.screen = screen
        self.advance_traps = []
        self.rule = rules.Rule()
        self.generator=SimpleTgenerator(self.screen, self.player, self.advance_traps, self.traps, self.rule)

    def update(self):


        self.generator.update()
        self.traps = [t for t in self.traps if t.is_active and t.life_time <= t.life_cycle]
        for trap in self.traps:
            trap.life_time += 1
            trap.update()

        for ad in self.advance_traps:
            ad.advance_Timer -= 1
            if ad.advance_Timer == 0:
                self.advance_traps.remove(ad)
                self.create_tarp(ad)

        self.check_collision(self.player.get_rect())


    def draw(self, screen):
        #陷阱绘制
        for trap in self.traps:
            trap.draw(screen)
        for ad in self.advance_traps:
            if len(self.advance_traps)>=5:
                ad.if_advance_time=False
            ad.advance_draw()

    def update_generator(self,generator):
        self.generator=generator(self.screen, self.player, self.advance_traps, self.traps, self.rule)

    def advance_create(self,ad):
        self.generator.advance_create(ad)

    def create_tarp(self, ad):
        self.traps.append(ad)

    def check_collision(self, player_rect):
        for tarp in self.traps:
            if tarp.rect.colliderect(player_rect):
                tarp.apply_damage()