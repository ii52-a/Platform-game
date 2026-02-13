from Manager.TrapGenerator.Basic_Tgenerator import Generator

from Trap import *
class ParadoxEidolon(Generator):

    def update(self):
        self.generator_counter += 1
        if self.generator_counter > self.generator_interval:
            self.advance_create()
            self.generator_counter = 0
            self.generator_interval=50

    def advance_create(self):
        pass


    def __str__(self):
        return "ParadoxEidolon_Tgenerator"