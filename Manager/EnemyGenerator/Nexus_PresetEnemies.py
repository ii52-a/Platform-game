from Effects import SlashEffect
from Enemy import TalkerFriend
from Manager.EnemyGenerator.Basic_Egenerator import Generator
from loop.Config import Screen


class NexusEGenerator(Generator):
    def __init__(self,enemyManager,player,screen,trapManager,platform):
        super().__init__(enemyManager,player,screen,trapManager,platform)
        self.once=True

    def update(self):
        if self.once:
            self.once=False
            for i in self.enemyManager.enemies:
                i.is_alive=False
                self.enemyManager.effects.append(SlashEffect(i.rect.x,i.rect.y,(0,0,0)))
            self.enemyManager.enemies.append(
                TalkerFriend(
                    screen=self.screen,
                    player=self.player,
                    name="模糊身形",
                    color=(0,0,0),
                    bottom=[Screen.ScreenX*3 //4,Screen.ScreenY-50]
                )
            )

    def generate(self):
        pass

    def __str__(self):
        return "Nexus庇护"







