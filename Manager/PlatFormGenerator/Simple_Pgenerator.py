import random

from Manager.PlatFormGenerator.Basic_Pgenerator import Generator
from PlatForm import *
from loop import rules


class SimpleGenerator(Generator):

    def __init__(self,platforms,rules):
        super().__init__(platforms,rules)



    #生成规则内核更新
    def update(self):
        self.generator_counter += 1  # 每帧增加
        generator_interval =100 -self.rules.stage *5
        if self.generator_counter >= generator_interval//2 and self.sp_once==True:
            self.generator_create_platform()
            self.sp_once=False
        if self.generator_counter >= generator_interval:
            self.sp_once=True
            self.generator_create_SIPplatform()
            self.generator_counter = 0



    #固定生成普通平台
    def generator_create_SIPplatform(self):

        stage=rules.Rule.stage
        """SIPHighPlatform, PlatformKSP, Platform,SpFragilePlatform,SPICEPlatform,SPICEPlatformQ,"""
        ot = []
        listt=[SIPHighPlatform, PlatformKSP, Platform, SpFragilePlatform, SPICEPlatform, SPICEPlatformQ]
        #region
        if stage == 1:
            ot = [30, 35, 25, 10]
        elif stage == 2:
            ot = [20, 40, 20, 20]
        elif stage == 3:
            ot = [25, 40, 20, 15]
        elif stage == 7:
            ot = [0, 5, 5, 5, 55, 30]
        elif stage == 8:
            ot = [40, 20, 20, 0, 10, 10]
        else:
            ot = [30, 35, 15, 20]
        # endregion
        if len(ot) < len(listt):
            ot += [0] * (len(listt) - len(ot))
        self.platforms.append(
            self.random_platform(listt,ot)
        )


    #特殊平台生成
    def generator_create_platform(self):


        """
            SpUpPlatform, SpDownPlatform, SpFragilePlatform,SPICEPlatform,SPICEPlatformQ,
        """
        stage=rules.Rule.stage
        ot = []
        listt=[SpUpPlatform, SpDownPlatform, SpFragilePlatform,SPICEPlatform,SPICEPlatformQ]
        if stage == 1:
            ot = [30, 35, 35]
        elif stage == 2:
            ot = [20, 60, 20]
        elif stage == 3:
            ot = [25, 50, 25]
        elif stage == 7:
            ot = [10, 10, 10, 30, 40]
        elif stage == 8:
            ot = [15, 15, 0, 40, 30]
        else:
            ot = [30, 40, 30]
        if len(ot) < len(listt):
            ot += [0] * (len(listt) - len(ot))
        self.platforms.append(
            self.random_platform(listt, ot)
        )

    def __str__(self):
        return "SimpleMap_PGenerator"