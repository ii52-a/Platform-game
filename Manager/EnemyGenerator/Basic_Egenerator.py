from abc import ABC, abstractmethod

from loop.rules import Rule


class Generator(ABC):
    def __init__(self,enemyManager,player,screen,trapManager,platform):
        self.enemyManager=enemyManager
        self.player = player
        self.screen = screen
        self.trapManager = trapManager
        self.platform = platform
        self.generator_interval=Rule.create_enemy_time()
        self.generator_counter=0

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def generate(self):
        raise NotImplementedError
