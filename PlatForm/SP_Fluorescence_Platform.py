import pygame.draw

from PlatForm import SIPrightMovePlatform


class SpFluorescencePlatform(SIPrightMovePlatform):
    def __init__(self):
        SIPrightMovePlatform.__init__(self)
        # self.color = (100, 100, 100)

    def draw(self,screen):
        super().draw(screen)
        if self.player:
            pygame.draw.circle(screen,(248, 255, 48),(self.player.pos[0],self.player.pos[1]),radius=self.player.radius+1,width=2)
        
