import random

from Trap import Laser


class LockLaser(Laser):
    def __init__(self, player, screen,color=(214, 212, 71),
                 advance_color=(255, 25, 25),advance_timer=175,damage=10,if_advance_time=True):
        super().__init__(player, screen,color=color,if_advance_time=if_advance_time)
        self.rect.x = max(min(random.randint(int(player.pos[0]) - 250, int(player.pos[0]) + 250),self.screen_pos_width-50),50)
        self.advance_speed_x = 0.8 + self.rule.stage * 0.3
        self.speed_x = 0
        self.life_cycle = 20 + 5 * self.rule.stage
        self.advance_Timer = advance_timer
        self.advance_color =advance_color
        self.damage = damage

    def advance_draw(self,color=(255, 25, 25)):
        if self.player.pos[0] > self.rect.x:
            self.rect.move_ip(min(self.advance_speed_x,2), 0)
        elif self.player.pos[0] < self.rect.x:
            self.rect.move_ip(max(-self.advance_speed_x,-2), 0)
        super().advance_draw(self.advance_color)