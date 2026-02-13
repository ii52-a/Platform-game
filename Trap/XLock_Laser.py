import random

from Trap.RectX_Laser import RectXLaser


class XLOCKLaser(RectXLaser):
    def __init__(self, player, screen,if_advance_time=True,advance_timer=175,damage=10,advance_speed_y=None):
        super().__init__(player, screen,if_advance_time=if_advance_time)
        self.rect.y = max(min(random.randint(int(player.pos[1]) - 100, int(player.pos[1]) + 100),self.screen_pos_height-30),30)
        self.advance_speed_y = 0.8 + self.rule.stage * 0.1 if advance_speed_y is None else advance_speed_y
        self.speed_y = 0
        self.life_cycle = 10 + 4 * self.rule.stage
        self.advance_Timer = advance_timer
        self.damage = damage
        self.life_cycle = 40

    def advance_draw(self):
        if self.player.pos[1] > self.rect.y:
            self.rect.move_ip(0,self.advance_speed_y)
        elif self.player.pos[1] <= self.rect.y:
            self.rect.move_ip(0,-self.advance_speed_y-2)
        super().advance_draw()