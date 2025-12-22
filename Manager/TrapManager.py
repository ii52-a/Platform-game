from loop import rules
from Trap import *

class TarpManager:
    def __init__(self, player, screen):
        self.tarps = []
        self.player = player
        self.create_counter = 0
        self.screen = screen
        self.advance_tarps = []
        self.rule = rules.Rule()

    def update(self):
        for p in self.tarps:
            if not p.is_active or p.life_time > p.life_cycle:
                self.tarps.remove(p)
                del p
            else:
                p.life_time += 1

        for platform in self.tarps:
            platform.update()
        self.check_collision(self.player.get_rect())

    def auto_create_tarp(self, time):
        self.create_counter += 1
        if self.create_counter > time:
            for _ in range(self.rule.trap_lack_num()):
                self.advance_create()
            self.create_counter = 0
        for ad in self.advance_tarps:
            ad.advance_Timer -= 1
            if ad.advance_Timer == 0:
                self.advance_tarps.remove(ad)
                self.create_tarp(ad)

    def draw(self, screen):
        for platform in self.tarps:
            platform.draw(screen)
        for ad in self.advance_tarps:
            if len(self.advance_tarps)>=4:
                ad.if_advance_time=False
            ad.advance_draw()

    def advance_create(self,ad=None):
        ad = self.rule.trap_create_rule([
            Laser, LockLaser, MoveLaser,RectXLaser,XLOCKLaser
        ])(self.player, self.screen) if ad is None else ad
        if ad:
            ad.advance_draw()
            self.advance_tarps.append(ad)

    def create_tarp(self, ad):
        self.tarps.append(ad)

    def check_collision(self, player_rect):
        for tarp in self.tarps:
            if tarp.rect.colliderect(player_rect):
                tarp.apply_damage()