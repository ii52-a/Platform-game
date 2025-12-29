import random
from abc import ABC, abstractmethod


class Generator(ABC):
    def __init__(self,platformManager,rules):
        self.rules = rules
        self.platformManager = platformManager
        self.platforms = platformManager.platforms
        self.generator_counter = 0
        self.sp_once=True


    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def generator_create_SIPplatform(self):
        raise NotImplementedError

    @abstractmethod
    def generator_create_platform(self):
        raise NotImplementedError


    #boss单独生成机制
    def boss_create_Platform(
                             self,platform_list:list,
                             ot_random:list
                             ):
        """
        :param platform_list: 平台类型
        :param ot_random: 对应平台的概率
        :return: None
        """
        self.platforms.append(self.random_platform(platform_list, ot_random))

    #随机生成器
    @staticmethod
    def random_platform(
                        platform_list:list,
                        ot_random:list
                        ):
        """
        :param platform_list: 随机类列表
        :param ot_random:  概率
        :return:  根据概率随机返回一个类，需要自行实例化
        """
        return random.choices(population=platform_list, weights=ot_random, k=1)[0]()




