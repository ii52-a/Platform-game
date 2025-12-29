from Manager.EnemyGenerator.Nexus_PresetEnemies import NexusEGenerator
from Manager.PlatFormGenerator.Nexus_PresetFoundations import NexusGenerator
from loop import rules
from loop.Config import Screen
from loop.rules import Rule
from Enemy import *

class StageController:
    def __init__(self,player,platform_manager,trap_manager,enemy_manager):
        self.mode = "normal"  # normal / nexus / boss
        self.player = player
        self.platformsManager = platform_manager
        self.trapsManager = trap_manager
        self.enemyManager = enemy_manager
        self.portal_active = False
        self.Boss=[True,True]
        self.boss=None

    def update(self):
        #normal 正常阶段
        if self.mode == "normal":
            #boss:BlackHole
            if Rule.get_stage() == 5 and self.Boss[0]:

                self.boss=BlackHole(self.enemyManager.screen, self.player, self.trapsManager, self.platformsManager,self.enemyManager)
                self.enemyManager.create_enemy(self.boss)
                self.enter_boss(1)
            #boss:IceBlue
            elif Rule.get_stage() == 8 and self.Boss[1]:
                self.enter_boss(2)
                self.boss=IceBlue(self.enemyManager.screen, self.player, self.trapsManager, self.platformsManager, self.enemyManager)
                self.enemyManager.create_enemy(self.boss)

        #过渡枢纽
        elif self.mode == "nexus":
            pass

        #boss阶段
        elif self.mode == "boss":
            if self.boss not in self.enemyManager.enemies:
                self.out_boss()
                if not self.Boss[1]:
                    self.enter_nexus()





    def enter_nexus(self):  #进入枢纽
        self.mode = "nexus"
        self.platformsManager.update_generator(NexusGenerator)
        self.enemyManager.update_generator(NexusEGenerator)
        self.player.pos[0]=Screen.ScreenX//2
        Rule.set_nexus("枢纽",(182, 182, 182))

    def enter_boss(self,boss_stage):
        self.mode="boss"
        self.Boss[boss_stage-1]=False
        Rule.if_boss = True
        Rule.boss_stage = boss_stage

    def out_boss(self):
        self.mode = "normal"
        self.boss=None

