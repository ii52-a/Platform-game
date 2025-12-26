from Manager.PlatFormGenerator import SimpleGenerator
from PlatForm import *

class BlackHoleGenerator(SimpleGenerator):
    def __init__(self, platforms, rules):
        super().__init__(platforms, rules)
        self.generator_counter = 0
        self.generator_interval = 0

    def update(self):
        pass

    def generator_create_platform(self):
        super().generator_create_platform()
        self.generator_counter += 1
        if self.generator_counter > self.generator_interval:
            self.platforms.boss_exPlatform()
            self.generator_counter = 0

    def generator_create_SIPplatform(self):
        pass


    def boss_exPlatform(self):
        self.platforms.append(self.rules.platform_boss_rule([
            SIPrightMovePlatform, SPrightFrpPlatform, SPICEPlatform, SPICEPlatformQ,
        ]))