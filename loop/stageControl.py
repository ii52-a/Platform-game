

from EffectGlobal import Global
from Enemy.Enemy_sp.BOSS import BlackHole
from Manager.EnemyGenerator.Nexus_PresetEnemies import NexusEGenerator
from Manager.EnemyGenerator.Simple_Egenerator import  SimpleEGenerator
from Manager.PlatFormGenerator import SimpleGenerator
from Manager.PlatFormGenerator.Boss_ParadoxEidolon_Pgenerator import ParadoxEidolonP
from Manager.PlatFormGenerator.Nexus_PresetFoundations import NexusGenerator
from Manager.TrapGenerator.Boss_ParadoxEidolon_Tgenerator import ParadoxEidolon
from PlatForm import SIPrightMovePlatform

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
        self.Boss=[True,True,True]
        self.final_Boss=[True,True,True]
        self.boss=None

        self.portal=False

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

            elif Rule.get_stage() ==9:
                if self.final_Boss[0]:
                    self.enter_boss(3)
                    self.trapsManager.update_generator(ParadoxEidolon)
                    self.platformsManager.update_generator(ParadoxEidolonP)
                    self.final_Boss[0] = False

        #过渡枢纽
        elif self.mode == "nexus":
            if Global.is_recall:
                self.enter_world("RecallWorld")
            if self.portal and self.p not in self.enemyManager.enemies:
                self.out_nexus()


        #boss阶段
        elif self.mode == "boss":
            if self.boss not in self.enemyManager.enemies:
                self.out_boss()
                if not self.Boss[1] and Rule.boss_stage==2:
                    self.enter_nexus()

        elif self.mode == "world":
            if not Global.is_recall:
                self.out_world()



    def enter_world(self,world_name):
        self.mode="world"

    def out_world(self):
        self.mode = "nexus"
        self.p= PortalFriend(
                self.enemyManager.screen, self.player, self.trapsManager, self.platformsManager,self.enemyManager
            )
        self.portal=True
        self.enemyManager.enemies.append(
           self.p
        )



    def enter_nexus(self):  #进入枢纽
        self.mode = "nexus"
        self.platformsManager.update_generator(NexusGenerator)
        self.enemyManager.update_generator(NexusEGenerator)
        self.player.pos[0]=Screen.ScreenX//2
        Rule.set_nexus("枢纽",(182, 182, 182))

    def out_nexus(self):
        self.platformsManager.update_generator(SimpleGenerator)
        self.enemyManager.update_generator(SimpleEGenerator)
        self.mode = "normal"
        Rule.out_nexus()

    def enter_boss(self,boss_stage):
        self.mode="boss"
        self.Boss[boss_stage-1]=False
        Rule.if_boss = True
        Rule.boss_stage = boss_stage

    def out_boss(self):
        self.mode = "normal"
        self.boss=None

