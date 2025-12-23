import random

from loop import rules
from PlatForm import *

class PlatformsManager:
    def __init__(self):
        self.platforms = []
        self.effects=[]
        self.spawn_counter = 0
        self.rules = rules.Rule()

    def update(self, spawn_interval):
        self.spawn_counter += 1  # 每帧增加
        # 显示当前计数器和间隔

        if self.spawn_counter >= spawn_interval:
            self.spawn_create_SIPplatform()
            if random.random() < 0.05 + 0.05 * self.rules.stage:
                self.spawn_create_platform()

            self.spawn_counter = 0  # 重置计数器
        for p in self.platforms:
            if not p.is_active:
                self.platforms.remove(p)
                del p
            else:
                p.update()
        for e in self.effects:
            if not e.is_alive:
                self.effects.remove(e)
                del e
            else:
                e.update()



    def spawn_create_SIPplatform(self):
        self.platforms.append(self.rules.sample_platform_create_rule(
            [SIPHighPlatform, PlatformKSP, Platform,SpFragilePlatform,SPICEPlatform,SPICEPlatformQ,]
        ))

    def spawn_create_platform(self):
        self.platforms.append(self.rules.platform_create_rule([
            SpUpPlatform, SpDownPlatform, SpFragilePlatform,SPICEPlatform,SPICEPlatformQ
        ]))

    def boss_exPlatform(self):
                self.platforms.append(self.rules.platform_boss_rule([
                    SIPrightMovePlatform,SPrightFrpPlatform,SPICEPlatform,SPICEPlatformQ,
                ]))

    def draw_all_platforms(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
        for effect in self.effects:
            effect.draw(screen)

    def check_collision(self, player_rect):
        for platform in self.platforms:
            if platform.check_collision((player_rect[0], player_rect[1]+player_rect[3],player_rect[2]-8,player_rect[3])):
                return platform
        return None
