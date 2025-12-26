import random

from loop.Config import Config, Show


class Rule:
    score = Config.INIT_SCORE
    stage = 1
    boss_stage=0
    if_boss=False
    @classmethod
    def get_stage(cls):
        # print(cls.stage)
        return cls.stage
    @classmethod
    def stage_change(cls, score):
        cls.score = score
        if cls.score < 150:
            cls.stage = 1
        elif 150 <= cls.score < 1400:
            cls.stage = 2
        elif score <= 2400:
            cls.stage = 3
        elif score <= 4500:
            cls.stage = 4
        elif score <= 10000:
            cls.stage = 5
        elif score <=15000:
            cls.stage = 6
        elif score <= 22000:
            cls.stage = 7
        elif score <= 50000:
            cls.stage = 8
        elif cls.score<=50000:
            cls.stage = 9
    def world_get(self):
        if self.stage == 1:
            return "白昼",(136, 137, 144)
        elif self.stage == 2:
            return "阴影",(176, 179, 200)
        elif self.stage == 3:
            return "起源",(59, 59, 59)
        elif self.stage == 4:
            return "迷惘",(76, 76, 76)
        elif self.stage == 5:
            return "红色黑洞",(255, 29, 29)
        elif self.stage == 6:
            return "炼狱",(255, 35, 29)
        elif self.stage == 7:
            return "浅蓝",(36, 233, 255)
        elif self.stage == 8:
            return "深蓝之海",(50, 71, 255)
        else:
            return "新世界",(0,0,0)

    @classmethod
    def again(cls):
        cls.score = 0
        cls.stage = 1
        cls.boss_stage = 0
        cls.if_boss = False
    """地图变化"""

    @classmethod
    def bg_color_get(cls):
        #纯白
        simple_color = (255, 255, 255)
        #地狱
        dy_color = (150, 24, 25)
        #灰色
        hs_color = (136, 136, 136)
        #高级灰
        gjh_color = (105, 105, 105)
        #冰蓝
        bl_color = (24, 145, 225)
        #深蓝之海
        sl_color =(0, 26, 255)
        if cls.stage == 1 or cls.stage == 3:
            return simple_color
        elif cls.stage == 2:
            return hs_color
        elif cls.stage == 4:
            return gjh_color
        elif cls.stage == 5:
            return dy_color if cls.if_boss else simple_color
        elif cls.stage == 6:
            return dy_color
        elif cls.stage == 7:
            return bl_color
        elif cls.stage == 8:
            return sl_color
        else:
            return simple_color

    """平台规则"""

    @classmethod
    def sample_platform_create_rule(cls,listt):
        """SIPHighPlatform, PlatformKSP, Platform,SpFragilePlatform,SPICEPlatform,SPICEPlatformQ,"""
        ot = []
        if cls.stage == 1:
            ot = [30, 35, 25, 10]
        elif cls.stage == 2:
            ot = [20, 40, 20, 20]
        elif cls.stage == 3:
            ot = [25, 40, 20, 15]
        elif cls.stage == 7:
            ot= [0,5,5,5,55,30]
        elif cls.stage == 8:
            ot=[40,20,20,0,10,10]
        else:
            ot = [30, 35, 15, 20]
        if len(ot) <len(listt):
            ot+=[0]*(len(listt)-len(ot))
        return random.choices(population=listt, weights=ot, k=1)[0]()


    @classmethod
    def trap_lack_num(cls):
        num = 0
        if cls.stage <= 2:
            num= 1
        elif cls.stage <= 4:
            num= 2
        elif cls.stage ==5 and not cls.if_boss:
            num= 3
        elif cls.stage == 5 and cls.if_boss:
            num= 1
        elif cls.stage <=6:
            num= 1
        elif cls.stage <=7:#浅蓝
            num= 1
        elif cls.stage <=8:  #深蓝之海
            num= 0
        else:
            num= 9
        return num+Show.TRAP_ADD

    @classmethod
    def create_enemy(cls,listt):
        ot = []
        if cls.stage <=4:
            ot = [30,70,0]
        elif cls.stage <=6:
            ot =[80,20,0]
        elif cls.stage <=7:
            ot =[5,5,90]
        elif cls.stage <=8:
            ot = [50,0,50]
        else:
            ot = [20,40,40]
        if len(ot) < len(listt):
            ot += [0] * (len(listt) - len(ot))
        return random.choices(population=listt, weights=ot, k=1)[0]

    @classmethod
    def create_enemy_time(cls):
        if cls.stage <= 8:
            return 300
        else:
            return 400


    @classmethod
    def platform_create_rule(cls,listt):
        """
            SpUpPlatform, SpDownPlatform, SpFragilePlatform,SPICEPlatform,SPICEPlatformQ,
        """
        ot = []
        if cls.stage == 1:
            ot = [30, 35, 35]
        elif cls.stage == 2:
            ot = [20, 60, 20]
        elif cls.stage == 3:
            ot = [25, 50, 25]
        elif cls.stage ==7:
            ot = [10, 10, 10, 30, 40]
        elif cls.stage == 8:
            ot = [15, 15, 0, 40, 30]
        else:
            ot = [30, 40, 30]
        if len(ot) < len(listt):
            ot+=[0]*(len(listt)-len(ot))
        return random.choices(population=listt, weights=ot, k=1)[0]()



    def trap_create_rule(self,listt):
        ot = []
        """
            Laser, LockLaser, MoveLaser,RectXLaser,XLOCKLaser
        """
        if self.stage == 1 or self.stage == 2:
            ot=[33,33,34,0]
        elif self.stage == 3:
            # ot = [40,20,35,5]
            ot=[1,4,5,90]
        elif self.stage == 4:
            # ot = [35,25,30,10]
            ot=[10,5,5,50,30]
        elif self.stage == 5 or self.stage == 6:
            ot = [20,20,30,25,5]
        elif self.stage == 7:
            ot = [20,20,10,20,30]
        else:
            ot = [20,20,20,20,20]
        if len(ot) < len(listt):
            ot+=[0]*(len(listt)-len(ot))
        return random.choices(population=listt, weights=ot, k=1)[0]

    @classmethod
    def platform_boss_rule(cls,listt):
        ot = []
        """SIPrightMovePlatform,SPrightFrpPlatform,SPICEPlatform,SPICEPlatformQ,"""
        if cls.boss_stage == 1:
            ot = [50,50]
        elif cls.boss_stage == 2:
            ot = [100]
        if len(ot) < len(listt):
            ot+=[0]*(len(listt)-len(ot))
        return random.choices(population=listt, weights=ot, k=1)[0]()

