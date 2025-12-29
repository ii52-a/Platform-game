from Manager.TrapGenerator.Basic_Tgenerator import Generator
from Trap import *

class SimpleTgenerator(Generator):
    def __init__(self,screen,player,advance_traps,traps,rules):
        super().__init__(screen=screen,player=player,advance_traps=advance_traps,traps=traps,rules=rules)



    def update(self):
        self.generator_counter += 1
        if self.generator_counter > self.generator_interval:
            for _ in range(self.rules.trap_lack_num()):
                self.advance_create()
            self.generator_counter = 0



    def advance_create(self,ad=None):
        ad = self.rules.trap_create_rule([
            Laser, LockLaser, MoveLaser,RectXLaser,XLOCKLaser
        ])(self.player, self.screen) if ad is None else ad
        if ad:
            self.advance_traps.append(ad)






