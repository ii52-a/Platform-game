import pygame

import enemy
import trap
from player import Player
from platform import PlatformsManager, PlatformFirst
from Event import Event
from message import Message
from trap import TarpManager,MoveLaser
import rules


class Game:
    PLATFORM_TIME = 100

    def __init__(self):
        # 初始化pygame

        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), vsync=True)
        self.rule = rules.Rule()
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()

        # 创建游戏对象
        self.running = True
        self.dt = 0

        self.now_stage = 1
        self.bg_color = self.rule.bg_color_get()

        #特殊事件实例
        self.platformsManager = PlatformsManager()

        self.message = Message()

        #初始平台

        self.platformsManager.platforms.append(PlatformFirst(Player.INIT_POS))
        self.platformsManager.spawn_create_platform()
        self.player = Player(self.platformsManager)
        self.trapManager = TarpManager(player=self.player, screen=self.screen)
        self.enemyManager = enemy.EnemyManager(self.player, self.screen,self.trapManager,self.platformsManager)
        self.event = Event(self.trapManager, self.screen)
        #设置参数

    def handle_events(self):
        """游戏进行事件检测"""
        if self.player.is_gaming:
            self.event.score_gain(10)
        if self.event.game_over(self.player.health):
            print(f"score:{self.event.score}")
            self.running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.is_downed()

    def update(self):
        """更新阶段变化"""

            # self.event.create_boss()
            # print(self.now_stage)

        """玩家效果"""
        # 更新玩家物理状态
        self.player.gravity_down()
        self.player.check_collision()
        keys = pygame.key.get_pressed()
        self.player.check_collision()
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.player.jump()
        if keys[pygame.K_a]:
            self.player.move(-self.player.speed)
        elif keys[pygame.K_d]:
            self.player.move(self.player.speed)

        self.platformsManager.update(self.PLATFORM_TIME - self.rule.stage * 8)
        self.trapManager.auto_create_tarp(180)
        self.trapManager.update()
        self.enemyManager.update()
        if self.now_stage != self.rule.stage:
            self.now_stage = self.rule.stage
            if self.now_stage == 4:
                for _ in range(5):
                    self.trapManager.advance_create(trap.Laser(self.player, self.screen))

    def render(self):
        # 绘制背景
        self.screen.fill(self.bg_color)

        # 玩家
        self.player.draw(self.screen)
        # 平台
        self.platformsManager.draw_all_platforms(self.screen)
        self.bg_color = self.rule.bg_color_get()
        #陷阱
        self.trapManager.draw(self.screen)
        # 显示信息
        self.render_debug_info()

        self.enemyManager.draw()

        # 更新显示
        pygame.display.flip()

    def render_debug_info(self):
        # 玩家信息
        vel_text_platform_count = len(self.platformsManager.platforms)
        vel_text_health = f"a0.7"
        vel_text_score = f" {self.event.score:.1f}"
        vel_text_stage = f"{self.rule.stage}"
        self.message.font_draw('platform_count:', vel_text_platform_count, self.screen, 10, 40)
        self.message.font_draw('version:', vel_text_health, self.screen, 10, 10)
        self.message.font_draw('score:', vel_text_score, self.screen, 10, 70)
        self.message.font_draw('stage:', vel_text_stage, self.screen, 10, 100)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()


# 启动游戏
if __name__ == "__main__":
    game = Game()
    game.run()
