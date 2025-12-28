import random

from Manager.PlatFormGenerator import SimpleGenerator
from loop import rules
from PlatForm import *

class PlatformsManager:
    def __init__(self):
        self.platforms = []
        self.effects=[]
        self.rules = rules.Rule()

        #规则内核
        self.generator=SimpleGenerator(self.platforms,self.rules)
    #region
    def update(self):
        if not self.generator:
            self.update_generator(SimpleGenerator(self.platforms,self.rules))
        self.generator.update()
        for p in self.platforms:
            if not p.is_active:
                self.platforms.remove(p)
                del p
            else:
                p.update()
        for e in self.effects:
            if not e.is_active:
                self.effects.remove(e)
                del e
            else:
                e.update()
    def update_generator(self,generator):
        self.generator = generator(self.platforms,self.rules)
        # print(self.generator)

    def draw_all_platforms(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
        for effect in self.effects:
            effect.draw(screen)

    def check_collision(self, player_rect):
        for platform in self.platforms:
            if platform.check_collision((player_rect[0], player_rect[1]+player_rect[3],player_rect[2]-8,player_rect[3])):
                return platform
        return None
    #endregion
