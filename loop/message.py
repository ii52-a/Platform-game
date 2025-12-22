
import pygame


class Message:

    def font_draw(self, name, text, screen, x, y, color=(0, 0, 0),font_size=16):
        default_font=pygame.font.SysFont("SimSun", font_size)
        vel_text = f"{name}{text}"
        vel_surface = default_font.render(vel_text, True, color)
        screen.blit(vel_surface, (x, y))
