import random

from Trap import Laser


class MoveLaser(Laser):

    def __init__(self, player, screen, speed_x=None,if_advance_time=True):
        super().__init__(player, screen)
        self.speed_x = random.randint(-1 * self.rule.stage, 1 * self.rule.stage) if speed_x is None else speed_x
        self.if_advance_time = if_advance_time
    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.rect.right < 20:
            self.is_active = False
        elif self.rect.right > self.screen_pos_width-20:
            self.is_active = False
        super().update()

    def advance_draw(self, if_advance_time=True):
        LorR = "Left" if self.speed_x < 0 else "Right"
        if self.if_advance_time:
            self.message.font_draw('', LorR, screen=self.screen,
                                   x=self.rect.x - 35, y=10,
                                   color=(160, 59, 163))
        super().advance_draw()