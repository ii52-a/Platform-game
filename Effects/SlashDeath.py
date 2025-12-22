import math
import random

import pygame



"""交叉双剑光 + 小碎块效果"""
class SlashEffect:
    def __init__(self, x, y, color=(255,255,255)):
        self.x, self.y = x, y
        self.color = color
        self.timer = 0
        self.duration = 120  # 持续20帧
        self.is_alive = True



        # 刀光的随机角度
        self.angle = random.randint(0, 180)
        # 产生一些向四周炸裂的小火花
        self.sparks = [
            {
                "pos": [x, y],
                "vel": [random.uniform(-8, 8), random.uniform(-8, 8)],
                "size": random.randint(4, 8)
            } for _ in range(12)
        ]

    def update(self):
        self.timer += 1
        # 更新火花
        for s in self.sparks:
            s["pos"][0] += s["vel"][0]
            s["pos"][1] += s["vel"][1]
            s["vel"][1] += 0.2  # 重力感

        if self.timer > self.duration:
            self.is_alive = False

    def draw(self, screen):
        if not self.is_alive: return

        # 1. 绘制“瞬时闪光”：两条交叉的极速斜线
        offset = 60 * (1 - self.timer / self.duration)  # 线条随时间缩短

        # 刀光1（顺时针旋转）
        p1 = (self.x - offset * math.cos(math.radians(self.angle)),
              self.y - offset * math.sin(math.radians(self.angle)))
        p2 = (self.x + offset * math.cos(math.radians(self.angle)),
              self.y + offset * math.sin(math.radians(self.angle)))

        # 刀光2（垂直于刀光1）
        p3 = (self.x - offset * math.cos(math.radians(self.angle + 90)),
              self.y - offset * math.sin(math.radians(self.angle + 90)))
        p4 = (self.x + offset * math.cos(math.radians(self.angle + 90)),
              self.y + offset * math.sin(math.radians(self.angle + 90)))

        # 绘制核心刀芒（白色粗线）
        pygame.draw.line(screen, (210, 210, 210), p1, p2, 4)
        pygame.draw.line(screen, (210, 210, 210), p3, p4, 4)

        # 2. 绘制喷溅火花
        for s in self.sparks:
            pygame.draw.circle(screen, self.color, (int(s["pos"][0]), int(s["pos"][1])), int(s["size"]))