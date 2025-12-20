import random
import threading

import pygame
import message
import trap
import rules
class Enemy:
    def __init__(self, screen, player, traps, platform, x=None, y=None, width=50, height=50, radius=None,
                 color=(0, 0, 0)):
        x = random.randint(0, 1280 - 1) if x is None else x
        y = random.randint(0, 720 - 1) if y is None else y
        self.radius = 20 if radius is None else radius

        self.health = 100
        self.damage = 10

        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 10

        self.screen = screen
        self.player = player
        self.init_color=color
        self.color = self.init_color

        self.message = message.Message()

        self.is_alive = True
        self.damage_time = 500
        self.damage_counter = 0
        self.trapManager = traps
        self.platform = platform



    def move(self):
        pass

    def update(self):
        pass

    def draw(self):
        w = self.radius if self.radius is not None else self.rect.width

        self.message.font_draw("HP", f"{self.health:.1f}", self.screen, self.rect.x + w, self.rect.y + 5, self.color)
        if self.radius is not None:
            pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y), radius=self.radius)
        else:
            pygame.draw.rect(self.screen, self.color, (self.rect.x, self.rect.y))


class EnemyManager:
    def __init__(self, player, screen, traps, platform):
        self.enemies = []
        self.player = player
        self.create_counter = 0
        self.screen = screen
        self.enemy_counter = 0
        self.rules = rules.Rule()
        self.FirstBoss = True
        self.trapManager = traps
        self.platform = platform

    def update(self, time=-1):
        # if time != -1:
        #     self.enemy_counter += 1
        #     if self.enemy_counter >= time:
        #         pass
        if self.rules.get_stage() == 5 and self.FirstBoss:
            self.rules.boss_stage = 1
            self.FirstBoss = False
            self.create_enemy(BossStageFirst(self.screen, self.player, self.trapManager, self.platform))

            rules.Rule.if_boss = True
        for p in self.enemies:
            if not p.is_alive:
                self.enemies.remove(p)
                del p
            else:
                p.update()

    def draw(self):
        for i in self.enemies:
            i.draw()

    def create_enemy(self, ad):
        self.enemies.append(ad)

    def check_collision(self, player_rect):
        pass


class BossStageFirst(Enemy):
    def __init__(self, screen, player, traps, platform):
        super().__init__(screen=screen, player=player, traps=traps, platform=platform)
        self.health = 300
        self.radius = 50
        self.rect.x = 640
        self.rect.y = 120
        self.damage_counter = 200
        self.if_tx = False
        self.tx_radius = self.radius
        self.create_platform_counter=0
        self.create_platform_cycle=130

    def update(self):
        rules.Rule.if_boss = True
        rules.Rule.boss_stage = 1
        self.damage_counter += 1
        if self.damage_counter >= self.damage_time:
            self.health -= 30
            self.call_laser()
            self.damage_counter = 0
        if self.health <= 0:
            self.is_alive = False
            rules.Rule.if_boss = False
        self.platform_create()

    def create_cycle(self):
        pygame.draw.circle(self.screen, (255, 37, 37), (self.rect.x, self.rect.y), radius=self.tx_radius, width=5)
        self.tx_radius += 5
        if self.tx_radius >= 200+(250-self.health):
            self.if_tx = False
            self.tx_radius = self.radius

    def draw(self):
        if self.if_tx:
            self.create_cycle()
        super().draw()

    def call_laser(self):
        fcolor = self.color
        self.color = (255, 37, 37)
        radius_c = self.radius
        self.radius = 60
        self.if_tx = True

        def l():
            self.radius = radius_c
            self.color = fcolor
            if self.color !=self.init_color:
                self.color = self.init_color

        threading.Timer(0.5, l).start()
        for _ in range(2):
            self.trapManager.advance_create(trap.Laser(screen=self.screen, player=self.player))

    def platform_create(self):
        self.create_platform_counter+=1
        if self.create_platform_counter > self.create_platform_cycle:
            self.platform.boss_exPlatform()
            self.create_platform_counter = 0
            self.trapManager.advance_create(trap.Laser(screen=self.screen, player=self.player))

    def __del__(self):
        for _ in range(5):
            self.trapManager.advance_create(trap.Laser(screen=self.screen, player=self.player))
