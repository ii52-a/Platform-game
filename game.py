import pygame

import enemy
import trap
from Config import Screen
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
        pygame.init()
        self.screen = pygame.display.set_mode((Screen.ScreenX, Screen.ScreenY), vsync=True)
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.if_reset=False
        self.history_max=0

        # 初始化游戏状态
        self.reset_game()

    def reset_game(self):
        """重置游戏到初始状态"""
        # 创建/重新创建游戏对象
        self.running = True
        self.dt = 0
        self.now_stage = 1

        # 重新创建游戏规则和实例
        self.rule = rules.Rule()
        self.rule.again()
        self.bg_color = self.rule.bg_color_get()

        # 重新创建所有游戏对象
        self.platformsManager = PlatformsManager()
        self.message = Message()

        # 初始平台
        self.platformsManager.platforms.append(PlatformFirst(Player.INIT_POS))
        self.platformsManager.spawn_create_platform()
        self.player = Player(self.platformsManager)
        
        self.player.pos = [Player.INIT_POS[0], Player.INIT_POS[1]]

        self.player.is_gaming = False
        self.player.velocity_y = 0
        self.trapManager = TarpManager(player=self.player, screen=self.screen)
        self.enemyManager = enemy.EnemyManager(self.player, self.screen, self.trapManager, self.platformsManager)
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
        """其他对象"""
        self.platformsManager.update(self.PLATFORM_TIME - self.rule.stage * 8)
        self.trapManager.auto_create_tarp(180)
        self.trapManager.update()
        self.enemyManager.update()

        #阶段更替
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
        vel_text_health = f"a2.7"
        vel_text_score = f" {self.event.score:.1f}"
        vel_text_stage = f"{self.rule.stage}"
        vel_text_history = f"{self.history_max}"
        self.message.font_draw('version:', vel_text_health, self.screen, 10, 10)
        self.message.font_draw("history:",vel_text_history,self.screen,10,40)
        self.message.font_draw('platform_count:', vel_text_platform_count, self.screen, 10, 70)
        self.message.font_draw('score:', vel_text_score, self.screen, 10, 100)
        self.message.font_draw('stage:', vel_text_stage, self.screen, 10, 130)

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
