import pygame

from loop.Config import Screen
from Trap.trap import Trap


class Laser(Trap):
    def __init__(self, player, screen, width=20, height=Screen.ScreenY, damage=10, color=(214, 212, 71),if_advance_time=True):
        self.color = color
        super().__init__(player=player, color=self.color, screen=screen, width=width, height=height, damage=damage)
        self.life_cycle = 60 + 2 * self.rule.stage
        self.if_advance_time=if_advance_time
        self.advance_tick=0

    def advance_draw(self,color=(255, 25, 25)):
        now=pygame.time.get_ticks()
        if self.if_advance_time and now-self.advance_tick>13:
            self.advance_tick=now
            self.message.font_draw('', f"{self.advance_Timer:.1f}", screen=self.screen, x=self.rect.x + self.rect.width,
                                   y=10,
                                   color=(210, 208, 120))
        pygame.draw.rect(self.screen, color, (self.rect.x + self.rect.width / 2, 0, 2, self.screen_pos_height))

    def update(self):
        self.life_time += 1
        if self.damage_time < self.damage_cycle:
            self.damage_time += 1

        if self.life_time > self.life_cycle:
            self.is_active = False

    def draw(self, screen):
        if self.if_advance_time:
            self.message.font_draw('', f"{self.life_cycle - self.life_time:.1f}", screen=self.screen,
                                   x=self.rect.x + self.rect.width + 5, y=10,
                                   color=(41, 230, 255))

        super().draw(screen)

    def apply_damage(self):
        if self.damage_time >= self.damage_cycle:
            self.player.is_damaging(self.damage)
            self.damage_time = 0