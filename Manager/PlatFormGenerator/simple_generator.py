import random

from Manager.PlatFormGenerator.generator import Generator
from PlatForm import *

class SimpleGenerator(Generator):

    def __init__(self,platforms,rules):
        super().__init__(platforms,rules)


    #生成规则内核更新
    def update(self):
        self.generator_counter += 1  # 每帧增加
        generator_interval =100
        if self.generator_counter >= generator_interval:
            self.generator_create_SIPplatform()
            if random.random() < 0.05 + 0.05 * self.rules.stage:
                self.generator_create_platform()
            self.generator_counter = 0

    #固定生成普通平台
    def generator_create_SIPplatform(self):
        self.platforms.append(self.rules.sample_platform_create_rule(
            [SIPHighPlatform, PlatformKSP, Platform, SpFragilePlatform, SPICEPlatform, SPICEPlatformQ, ]
        ))

    #特殊平台生成
    def generator_create_platform(self):
        self.platforms.append(self.rules.platform_create_rule([
            SpUpPlatform, SpDownPlatform, SpFragilePlatform, SPICEPlatform, SPICEPlatformQ
        ]))