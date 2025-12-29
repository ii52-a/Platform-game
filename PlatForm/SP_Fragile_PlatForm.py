"""易碎平台"""
from PlatForm.Basic_Platform import Platform


class SpFragilePlatform(Platform):
    def __init__(self,first_color=(222, 233, 26),second_color=(207, 74, 74)):
        super().__init__()
        self.is_player = None
        self.destroy_time = 120 - self.rule.stage * 10  ###
        self.destroy_counter = 0
        self.destroy_now = False
        self.first_color = first_color
        self.second_color = second_color

    def update(self):
        super().update()
        if self.if_player and not self.destroy_now:
            self.color = self.first_color
            self.destroy_now = True
        if self.destroy_counter > self.destroy_time / 2:
            self.color = self.second_color
        if self.destroy_now:
            self.self_destroy()

    def self_destroy(self):
        self.destroy_counter += 1
        if self.destroy_counter > self.destroy_time:
            self.is_player = None
            self.is_active = False

    def draw(self, screen):
        super().draw(screen)
        if self.destroy_now:
            self.message.font_draw("", f"{self.destroy_time - self.destroy_counter}", screen,
                                   self.rect.x + self.width + 5, self.rect.y - 10, self.color)
