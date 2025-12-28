import pygame
import random
from EffectGlobal import Global


class BossDeathEffect:

    def __init__(self, x, y, color=(255, 50, 50),func=None):
        self.x, self.y = x, y
        self.color = color
        self.timer = 0
        self.duration = 200  # 总时长
        self.is_active = True
        self.func = func

        # 产生碎片
        self.particles = []
        for _ in range(40):
            self.particles.append({
                "pos": [x, y],
                "vel": [random.uniform(-10, 10), random.uniform(-10, 10)],
                "size": random.randint(4, 8)
            })

    def update(self):
        self.timer += 1

        if self.timer ==2:
            Global.shark_time = 12

        for p in self.particles:
            if self.timer < 40:  # 初始扩散
                p["pos"][0] += p["vel"][0]
                p["pos"][1] += p["vel"][1]
            elif self.timer < 70:
                dx = self.x - p["pos"][0]
                dy = self.y - p["pos"][1]
                p["pos"][0] += dx * 0.1
                p["pos"][1] += dy * 0.1
            else:
                if self.timer <= 81:
                    Global.shark_time = 4
                p["pos"][0] += p["vel"][0] * 3
                p["pos"][1] += p["vel"][1] * 3

        if self.timer >= self.duration:
            self.is_active = False
            Global.shark_time = 0


    def draw(self, screen):
        if 70 < self.timer < 85:
            # ?
            pass

        for p in self.particles:
            pygame.draw.circle(screen, self.color, (int(p["pos"][0]), int(p["pos"][1])), int(p["size"]))

        if self.timer > 70:
            r = (self.timer - 70) * 15
            thickness = max(1, 15 - (self.timer - 70) // 2)
            pygame.draw.circle(screen, (126, 0, 0), (self.x, self.y), r, thickness)