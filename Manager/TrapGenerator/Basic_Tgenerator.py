from abc import ABC, abstractmethod


class Generator(ABC):
    def __init__(self,screen,player,advance_traps,traps,rules):
        self.rules = rules
        self.traps = traps
        self.advance_traps = advance_traps
        self.screen = screen
        self.player = player
        self.generator_interval=180
        self.generator_counter=0




    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def advance_create(self):
        raise NotImplementedError

