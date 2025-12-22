import pygame

import message

from loop.Config import Screen, Config


class Player:
    INIT_POS = [400, 300]  #初始位置

    def __init__(self, platformmanager):
        # 属性
        self.health = Config.PLAYER_HEALTH  #生命值
        self.pos = self.INIT_POS  #坐标

        self.speed = 7  # 初始速度

        self.radius = 20
        self.color = (5, 5, 5)
        self.velocity_y = 0  # 垂直速度
        self.jump_power = 1.5  # 跳跃增量
        self.jump_speedMax = -14  # 最大速度
        self.gravity = 1.4  # 重力加速度

        #状态
        self.is_gaming = False
        self.is_jumping = False
        self.is_downJumping = False
        self.is_grounded = True
        self.platformManager = platformmanager
        self.current_platform = self.platformManager.platforms[0]  # 绑定初始平台
        self.message = message.Message()

        self.damage_color=0

        self.fcolor=(5,5,5)

    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - self.radius,
            self.pos[1] - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    """玩家绘制"""

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        self.message.font_draw("HP:", f"{self.health:.1f}", screen=screen, color=self.color, x=self.pos[0] - 30,
                               y=self.pos[1] - 40)

    """左右限制"""

    def left_right_limit(self):
        if self.pos[0] + self.radius >= Screen.ScreenX:
            self.pos[0] = Screen.ScreenX - self.radius
        elif self.pos[0] - self.radius <= 0:
            self.pos[0] = 0 + self.radius


    """离开平台，用于增加平台交互"""

    def height_limit(self):
        if self.pos[1] - self.radius <=0:
            if self.is_grounded:
                self.leave_platform()
            self.pos[1] =0+self.radius
    def leave_platform(self):
        self.current_platform.debind_player()
        self.current_platform.if_player = False
        self.current_platform = None
        self.is_grounded = False

    """绑定平台"""

    def check_collision(self):
        if self.current_platform and not self.current_platform.is_active:
            self.leave_platform()
        if self.current_platform is None:
            platform = self.platformManager.check_collision(self.get_rect())
            if platform and self.velocity_y >0:
                self.is_grounded = True
                self.current_platform = platform
                self.current_platform.if_player = True
                self.current_platform.bind_player(self)
                self.current_platform.last_pos = (self.current_platform.rect.x, self.current_platform.rect.y)
        if self.is_grounded:
            pos = self.pos
            rad = self.radius
            cx = self.current_platform.rect.x
            cw = self.current_platform.width
            if pos[0] - rad > cx + cw or pos[0] + rad < cx - 5:
                self.leave_platform()
            # print(self.current_platform)

    def jump(self):
        #检查跳跃状态

        if not self.is_downJumping:
            if not self.is_gaming:
                self.is_gaming = True
                self.current_platform.is_gaming = True
            if self.is_grounded:
                self.leave_platform()
            self.is_jumping = True
            # 根据跳跃累加速度
            if self.velocity_y == 0:
                self.velocity_y = -3
            if self.velocity_y >= self.jump_speedMax:
                self.velocity_y -= self.jump_power * self.gravity
            # 进入下降状态,无法跳跃
            if self.velocity_y < self.jump_speedMax or self.velocity_y > 0:
                self.is_downJumping = True

    def is_downed(self):
        self.is_downJumping = True

    def move(self, speed):
        if not self.is_gaming:
            self.is_gaming = True
            self.current_platform.is_gaming = True
        if speed:
            self.pos[0] += speed
            self.left_right_limit()

    def is_damaging(self, damage, color=(255, 44, 44)):
        if self.is_gaming:
            if self.color == self.fcolor:
                self.color = color
                self.damage_color=pygame.time.get_ticks()
            self.health -= damage

    def init_color(self):
        self.color = self.fcolor




        # TODO
        pass

    def gravity_down(self):
        self.height_limit()
        if not self.is_grounded:
            self.pos[1] += self.velocity_y
            if self.velocity_y < -self.jump_speedMax:
                self.velocity_y += self.gravity
            #衰落死亡
            if self.pos[1] >= 1000:
                if not Config.PLAYER_NO_DAMP:
                    self.health = 0
                else:
                    self.pos[1] = 200

        if self.current_platform:
            self.velocity_y = 0
            self.pos[1] = self.current_platform.rect.y - self.radius
            self.pos[0] += self.current_platform.rect.x - self.current_platform.last_pos[0]
            self.current_platform.last_pos = [self.current_platform.rect.x, self.current_platform.rect.y]
            self.left_right_limit()
            self.is_grounded = True
            self.is_jumping = False
            self.is_downJumping = False
        else:
            self.is_grounded = False
