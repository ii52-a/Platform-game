import random
import pygame


class LightningEffect:
    """
    闪电特效
    """
    def __init__(self, start_pos, end_pos, duration=20, color=(100, 149, 237)):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.color = color
        self.is_active = True
        self.points = self._generate_points()

    def _generate_points(self):
        pts = [self.start_pos]
        num = 5
        dx = (self.end_pos[0] - self.start_pos[0]) / num
        dy = (self.end_pos[1] - self.start_pos[1]) / num

        for i in range(1, num):
            dtx = random.randint(-15, 15)
            dty = random.randint(-15, 15)
            px = self.start_pos[0] + dx * i + dtx
            py = self.start_pos[1] + dy * i + dty
            pts.append((px, py))

        pts.append(self.end_pos)
        return pts

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.is_active = False
        self.points = self._generate_points()

    def draw(self, screen):
        if len(self.points) > 1:
            pygame.draw.lines(screen, self.color, False, self.points, 3)
            pygame.draw.lines(screen, self.color, False, self.points, 1)