from Manager.PlatFormGenerator import  SimpleGenerator
from PlatForm import *
from PlatForm.SP_Fluorescence_Platform import SpFluorescencePlatform


class ParadoxEidolonP(SimpleGenerator):
    def __init__(self, platforms, rules):
        super().__init__(platforms, rules)
        self.generator_interval=100

    def boss_clear(self):
        self.platforms=[]


    def update(self):
        self.generator_counter += 1
        if self.generator_counter > self.generator_interval:
            self.generator_create_platform()
            self.generator_counter = 0

    def generator_create_platform(self):
        platform_list=[SpFluorescencePlatform]
        self.platforms.append(platform_list[0]())

    def generator_create_SIPplatform(self):
        pass

