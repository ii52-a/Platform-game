"""上升平台"""
from PlatForm.platform import Platform


class SpUpPlatform(Platform):
    def __init__(self):

        super().__init__(color=(25, 60, 80))

    def update(self):
        add_x = self.speed_x
        add_y = self.speed_y
        if self.is_active:
            if self.if_player:
                self.speed_x += -0.5 - 0.2 * self.rule.stage
                self.speed_y += -0.2 - self.rule.stage * 0.5
            self.rect.x -= self.speed_x
            self.rect.y += self.speed_y
        self.speed_x = add_x
        self.speed_y = add_y
        if self.rect.x < 0 - self.width or self.rect.y > 720 + self.height:
            self.is_active = False

    def draw(self, screen):
        super().draw(screen)
        self.message.font_draw("", "UP", screen, self.rect.x + self.width + 5, self.rect.y - 10, (225, 45, 3))
