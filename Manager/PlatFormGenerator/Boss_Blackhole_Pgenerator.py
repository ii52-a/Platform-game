from Manager.PlatFormGenerator import SimpleGenerator
from PlatForm import *


class BlackHoleGenerator(SimpleGenerator):
    def __init__(self, platforms, rules):
        super().__init__(platforms, rules)
        self.generator_boss_counter = 0
        self.generator_boss_interval = 100

    def update(self):
        super().update()
        self.generator_boss_counter += 1
        if self.generator_boss_counter >= self.generator_boss_interval:
            self.boss_exPlatform()
            self.generator_boss_counter = 0



    def generator_create_platform(self):
        super().generator_create_platform()


    def generator_create_SIPplatform(self):
        super().generator_create_SIPplatform()


    def boss_exPlatform(self):
        platform_list=[SIPrightMovePlatform,SPrightFrpPlatform]
        ot_random=[50,50]
        self.boss_create_Platform(platform_list,ot_random)

    def __str__(self):
        return "BlueHole_PGenerator"