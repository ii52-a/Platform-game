import random

import pygame

from EffectGlobal import Global
from Manager import *

from loop.Config import Screen, Version, Config
from PlatForm import PlatformFirst, PlatformControl
from player import Player
from loop.Event import Event
from message import Message
from loop.rules import Rule
from Trap import *

class Game:
    PLATFORM_TIME = 100

    def __init__(self):
        # 初始化pygame
        pygame.init()
        pygame.display.set_caption("Game")
        self.event = None
        self.enemyManager = None
        self.trapManager = None
        self.player = None
        self.message = None
        self.platformsManager = None
        self.bg_color = None
        self.rule = None
        self.now_stage = None
        self.dt = None
        self.running = None
        #屏幕
        self._display = pygame.display.set_mode((Screen.ScreenX, Screen.ScreenY), vsync=True)
        #时刻钟
        self.clock = pygame.time.Clock()
        #历史
        self.history_max=0
        #屏幕位移 / 震屏打击
        self.game_canvas = pygame.Surface((Screen.ScreenX, Screen.ScreenY))
        self.screen=self.game_canvas
        self.shake_amount=0

        # 初始化游戏状态
        self.reset_game()

    def reset_game(self):
        self.running = True
        self.dt = 0
        self.now_stage = 1

        # 重新创建游戏规则和实例
        self.rule = Rule()
        self.rule.again()
        self.bg_color = self.rule.bg_color_get()


        # 重新创建所有游戏对象
        self.platformsManager = PlatformsManager()
        self.platformsManager.spawn_create_platform()
        self.player = Player(self.platformsManager)

        self.player.pos = [Player.INIT_POS[0], Player.INIT_POS[1]]

        self.player.is_gaming = False
        self.player.velocity_y = 0
        self.message = Message()

        # 初始平台
        first = PlatformFirst(Player.INIT_POS)
        if Config.TEST_PLATFORM:
            first=PlatformControl(self.player)
            self.player.is_gaming=True

        self.player.current_platform=first
        self.platformsManager.platforms.append(first)

        self.trapManager = TarpManager(player=self.player, screen=self.screen)
        self.enemyManager = EnemyManager(self.player, self.screen, self.trapManager, self.platformsManager)
        self.event = Event(self.trapManager, self.screen)




    def handle_events(self):
        """游戏进行事件检测"""
        if self.player.is_gaming:
            self.event.score_gain(10)
        if self.event.game_over(self.player.health):
            print(f"score:{self.event.score}")
            self.history_max=max(self.history_max, self.event.score)
            self.reset_game()

            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.is_downed()

            elif event.type == pygame.KEYDOWN and not Config.TEST_PLATFORM:
                if event.key == pygame.K_s:
                    self.player.down()

    def update(self):
        """更新阶段变化"""


        """玩家效果"""
        # 更新玩家物理状态
        self.player.gravity_down()
        self.player.check_collision()
        keys = pygame.key.get_pressed()
        self.player.check_collision()
        if Config.TEST_PLATFORM:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                self.player.pos[1] -=8
            if keys[pygame.K_s] and Config.TEST_PLATFORM:
                self.player.pos[1] += 8
            if keys[pygame.K_a]:
                self.player.pos[0] -=8
            elif keys[pygame.K_d]:
                self.player.pos[0] += 8
        else:
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                self.player.jump()

            if keys[pygame.K_a]:
                self.player.move(-self.player.speed)
            elif keys[pygame.K_d]:
                self.player.move(self.player.speed)
        """平台和陷阱"""
        self.platformsManager.update(self.PLATFORM_TIME - self.rule.stage * 8)
        self.trapManager.auto_create_tarp(180)
        self.trapManager.update()
        self.enemyManager.update()

        #阶段更替
        if self.now_stage != self.rule.stage:
            self.now_stage = self.rule.stage
            if self.now_stage == 4:
                for _ in range(5):
                    self.trapManager.advance_create(Laser(self.player, self.screen))
            if self.now_stage == 8:
                self.player.speed+=5

        #玩家变化
        ck=pygame.time.get_ticks()
        if ck-self.player.damage_color >500:
            self.player.init_color()

        #屏幕打击感
        if Global.shark_time>self.shake_amount:
            self.shake_amount=Global.shark_time
            Global.shark_time = 0
        if self.shake_amount > 0:
            self.shake_amount -= 1  # 每帧减少打击
            if self.shake_amount < 0:
                self.shake_amount = 0

    def render(self):
        # 绘制背景
        self.game_canvas.fill(self.bg_color)

        self.player.draw(self.game_canvas)
        self.platformsManager.draw_all_platforms(self.game_canvas)
        self.trapManager.draw(self.game_canvas)
        self.enemyManager.draw()
        self.bg_color = self.rule.bg_color_get()
        # 震动参数
        offset_x = 0
        offset_y = 0
        if self.shake_amount > 0:
            offset_x = random.randint(-int(self.shake_amount), int(self.shake_amount))
            offset_y = random.randint(-int(self.shake_amount), int(self.shake_amount))
        self._display.fill((0, 0, 0))
        self._display.blit(self.game_canvas, (offset_x, offset_y))
        # 显示信息
        self.render_debug_info()

        # 更新显示
        pygame.display.flip()

    def render_debug_info(self):
        # 玩家信息
        vel_text_platform_count = len(self.platformsManager.platforms)
        vel_text_health = f"{Version.VERSION_STR}"
        vel_text_score = f" {self.event.score:.1f}"
        vel_text_stage = f"{self.rule.stage}"
        vel_text_history = f"{self.history_max}"
        vel_text_world=f"{self.rule.world_get()[0]}"
        vel_text_world_color=self.rule.world_get()[1]
        self.message.font_draw('version:', vel_text_health, self._display, 10, 10)
        self.message.font_draw("history:",vel_text_history,self._display,10,40)
        self.message.font_draw('platform_count:', vel_text_platform_count, self._display, 10, 70)
        self.message.font_draw('world:',vel_text_world,self._display,10,100,color=vel_text_world_color)
        self.message.font_draw('score:', vel_text_score, self._display, 10, 130)
        self.message.font_draw('stage:', vel_text_stage, self._display, 10, 160)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.dt = self.clock.tick(60) / 1000


        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
