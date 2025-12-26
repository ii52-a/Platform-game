from abc import ABC, abstractmethod


class Generator(ABC):
    def __init__(self,platforms,rules):
        self.rules = rules
        self.platforms = platforms
        self.generator_counter = 0

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def generator_create_SIPplatform(self):
        raise NotImplementedError

    @abstractmethod
    def generator_create_platform(self):
        raise NotImplementedError


    def boss_exPlatform(self):
        pass


