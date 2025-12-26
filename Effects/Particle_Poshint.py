import math
import random

import pygame


class ParticlePoint:
    def __init__(self, start_pos, end_pos, scatter_time, travel_time, radius, color=(255, 255, 255)):
        self.pos = pygame.Vector2(start_pos)
        self.end_pos = pygame.Vector2(end_pos)

        # 阶段时间控制（帧数）
        self.scatter_time = scatter_time  # 散射持续多久（例如 20 帧）
        self.travel_time = travel_time  # 飞行持续多久（例如 40 帧）
        self.current_frame = 0

        # 散射阶段的随机初速度
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(5, 12)
        self.vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)

        self.color = color
        self.radius = radius
        self.is_alive = True

        # 记录散射结束时的位置，作为第二阶段的起点
        self.mid_pos = None

    def update(self):
        self.current_frame += 1


        if self.current_frame <= self.scatter_time:
            self.pos += self.vel
            self.vel *= 0.96


            if self.current_frame == self.scatter_time:
                self.mid_pos = pygame.Vector2(self.pos)


        elif self.current_frame <= (self.scatter_time + self.travel_time):

            t = (self.current_frame - self.scatter_time) / self.travel_time

            eased_t = t * t


            self.pos = self.mid_pos.lerp(self.end_pos, eased_t)

        else:
            self.is_alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)