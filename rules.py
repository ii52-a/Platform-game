import random


class Rule:
    score = 0
    stage = 1
    boss_stage=0
    if_boss=False

    def __init__(self):
        pass

    @classmethod
    def get_stage(cls):
        return cls.stage
    @classmethod
    def stage_change(cls, score):
        cls.score = score
        if cls.score < 150:
            cls.stage = 1
        elif 150 <= cls.score < 750:
            cls.stage = 2
        elif score <= 1500:
            cls.stage = 3
        elif score <= 3500:
            cls.stage = 4
        elif score <= 10000:
            cls.stage = 5
        elif score <=50000:
            cls.stage = 6

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
        return None

    """平台规则"""

    @classmethod
    def sample_platform_create_rule(cls,listt):
        ot = []
        if cls.stage == 1:
            ot = [30, 35, 25, 10]
        elif cls.stage == 2:
            ot = [20, 40, 20, 20]
        elif cls.stage == 3:
            ot = [25, 40, 20, 15]
        else:
            ot = [30, 35, 15, 20]
        return random.choices(population=listt, weights=ot, k=1)[0]()


    @classmethod
    def trap_lack_num(cls):
        if cls.stage <= 2:
            return 1
        elif cls.stage <= 4:
            return 2
        elif cls.stage ==5 and not cls.if_boss:
            return 3
        elif cls.stage == 5 and cls.if_boss:
            return 1
        elif cls.stage <=6:
            return 3
        return None

    @classmethod
    def platform_create_rule(cls,listt):
        ot = []
        if cls.stage == 1:
            ot = [30, 35, 35]
        elif cls.stage == 2:
            ot = [20, 60, 20]
        elif cls.stage == 3:
            ot = [25, 50, 25]
        else:
            ot = [30, 40, 30]
        return random.choices(population=listt, weights=ot, k=1)[0]()

    @classmethod
    def platform_boss_rule(cls,listt):
        ot = []
        if cls.boss_stage == 1:
            ot = [50,50]
        return random.choices(population=listt, weights=ot, k=1)[0]()

    def create_boss(self,tt):
        if self.stage == 5:
            return tt
        return None

    def trap_create_rule(self,listt):   #Laser, LockLaser, MoveLaser
        ot = []
        if self.stage == 1 or self.stage == 2:
            ot=[33,33,34,0]
        elif self.stage == 3:
            # ot = [40,20,35,5]
            ot=[1,1,1,97]
        elif self.stage == 4:
            # ot = [35,25,30,10]
            ot=[1,1,1,97]
        elif self.stage == 5:
            ot = [30,25,30,15]
        else:
            ot = [25,30,20,25]
        return random.choices(population=listt, weights=ot, k=1)[0]
