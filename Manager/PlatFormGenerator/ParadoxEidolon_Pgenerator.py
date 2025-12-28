from Manager.PlatFormGenerator import Generator


class ParadoxEidolon(Generator):
    def __init__(self, platforms, rules):
        super().__init__(platforms, rules)
        self.boss_clear()

    def boss_clear(self):
        self.platforms=[]


    def update(self):
        pass

    def generator_create_platform(self):
        pass

    def generator_create_SIPplatform(self):
        pass

