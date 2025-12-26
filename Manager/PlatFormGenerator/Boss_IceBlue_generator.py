from Manager.PlatFormGenerator.generator import Generator
from PlatForm import *

class IceBlueGenerator(Generator):
    def __init__(self,platforms,rules):
        super().__init__(platforms,rules)

    def generator_create_platform(self):
        pass

    def generator_create_SIPplatform(self):
        pass

    def update(self):
        pass

    def boss_exPlatform(self):
        self.platforms.append(self.rules.platform_boss_rule([
            SIPrightMovePlatform, SPrightFrpPlatform, SPICEPlatform, SPICEPlatformQ,
        ]))

