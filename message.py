import pygame


class Message:
    def __init__(self):
        self.default_font = pygame.font.SysFont(None, 24)

    def font_draw(self, name, text, screen, x, y, color=(0, 0, 0)):
        vel_text = f"{name}{text}"
        vel_surface = self.default_font.render(vel_text, True, color)
        screen.blit(vel_surface, (x, y))
