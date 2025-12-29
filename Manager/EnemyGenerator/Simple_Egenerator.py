from Manager.EnemyGenerator.Basic_Egenerator import Generator
from Enemy import *
from loop.rules import Rule


class SimpleGenerator(Generator):
    def __init__(self,enemies,player,screen,trapManager,platform):
        super().__init__(enemies,player=player,screen=screen,trapManager=trapManager,platform=platform)
    def update(self):
        self.generator_counter+=1
        if self.generator_counter >= self.generator_interval:
            self.generator_counter = 0
            self.generate()


    def generate(self):
        self.enemyManager.enemies.append((Rule.create_enemy(
            [TreatEnemy, BlackEnemy, IceEnemy]
        ))(self.screen, self.player, self.trapManager, self.platform, self.enemyManager))


    def __str__(self):
        return "SimpleMap_Egenerator"