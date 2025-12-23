import pygame





class CycleDeath:
    """
    圆波扩散
    """
    def __init__(self, x, y,
                 color=(32, 32, 238),max_radius=90,speed=3,thickness=6
                 ):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.max_radius = max_radius  # 扩散多大
        self.speed = speed  # 扩散多快
        self.thickness = thickness  # 初始线条粗细
        self.is_alive = True

    def update(self):
        self.radius += self.speed
        self.thickness = max(1, 6 - int((self.radius / self.max_radius) * 6))

        if self.radius >= self.max_radius:
            self.is_alive = False

    def draw(self, screen):
        if self.is_alive:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)