import random

import pygame

from EffectGlobal import Global
from loop import rules
from loop.Config import Config, Screen
from Enemy import Enemy, IceEnemy

"""冰蓝"""
class IceBlue(Enemy):
    def __init__(self, screen, player, traps, platform,enemy):
        super().__init__(screen=screen, player=player, traps=traps, platform=platform,enemy=enemy)
        self.fhealth = Config.SECOND_BOSS_HEALTH
        self.health = self.fhealth
        self.color=(0, 10, 103)
        self.radius = 50
        self.rect.x = 640
        self.rect.y = 120



        #技能
        self.damage_counter = 120
        self.damage_time =Config.SECONDE_BOSS_INTERNAL


        #平台生成
        self.create_platform_counter=0
        self.create_platform_cycle=130

        #深蓝打击
        self.trapt=[]

        #过渡技能
        self.first_once=True

        #位移动量
        self.dx=0
        self.dy=0


        #碰撞自我扣血
        self.cz_self_damage=3

        #碰撞玩家扣血
        self.pz_damage=5
        #碰撞冷却
        self.damage_player_counter=0

        self.lock={}




    def update(self):
        rules.Rule.if_boss = True
        rules.Rule.boss_stage = 2
        self.damage_counter += 1
        if self.damage_counter >= self.damage_time:
            self.health -=10
            # 第一阶段
            if self.health >= self.fhealth*3//4:
                k_num=(self.fhealth-self.health) //10
                for _ in range(2):
                    self.enemyManager.enemies.append(self.create_new_enemy(IceEnemy))
                for i in range(k_num):
                    #深蓝打击
                    new_trap = {
                        "pos": (random.randint(50, Screen.ScreenX - 50), random.randint(50, Screen.ScreenY - 50)),
                        "radius": 10,
                        "color": (23, 255, 228)
                    }
                    self.trapt.append(new_trap)
            #切换 过渡技能
            if self.health <= self.fhealth*3//4 and self.first_once:
                self.dx=10
                self.dy=10
                for _ in range(3):
                    self.enemyManager.enemies.append(self.create_new_enemy(IceEnemy))
                #加快施法
                self.damage_counter -=40
                self.create_platform_counter-=10
                self.cz_self_damage =2
                self.first_once=False
            #第二阶段
            elif self.health >= self.fhealth//2:
                self.health-=5
                for _ in range(2):
                    self.enemyManager.enemies.append(self.create_new_enemy(IceEnemy))
                dextra=(self.fhealth-self.health)//5
                self.dx =random.randint(-12-dextra,12+dextra)
                self.dy = random.randint(-6-dextra,6+dextra)
                for _ in range(7):
                    self.trapt.append({
                        "pos": (random.randint(50, Screen.ScreenX - 50), random.randint(50, Screen.ScreenY - 50)),
                            "radius": 5,
                            "color": (4, 148, 131)
                    })
            else:
                dextra=(self.fhealth-self.health)//10
                self.dx =random.randint(-12-dextra,12+dextra)
                self.dy = random.randint(-6-dextra,6+dextra)
                for _ in range(8):
                    self.trapt.append({
                        "pos": (random.randint(50, Screen.ScreenX - 50), random.randint(50, Screen.ScreenY - 50)),
                            "radius": 5,
                            "color": (4, 148, 131)
                    })
            self.damage_counter = 0
        if abs(self.dx)>1 or abs(self.dy)>1:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.dx *=0.98
            self.dy *=0.98
        if self.rect.x-self.radius <=0:
            self.rect.x =self.radius
            self.dx *=-1.02
            self.health -=self.cz_self_damage
        if self.rect.x+self.radius >= Screen.ScreenX:
            self.rect.x = Screen.ScreenX-self.radius
            self.dx *=-1.02
            self.health -=self.cz_self_damage
        if self.rect.y+self.radius >= Screen.ScreenY:
            self.rect.y = Screen.ScreenY-self.radius
            self.dy *=-1.02
            self.health -= self.cz_self_damage
        if self.rect.y-self.radius <= 0:
            self.rect.y = self.radius
            self.dy *=-1.02
            self.health -= self.cz_self_damage
        if self.health <= 0:
            self.is_alive = False
            rules.Rule.if_boss = False
        now=pygame.time.get_ticks()
        if self.rect.colliderect(self.player.get_rect()) and now-self.damage_player_counter>=100:
            self.player.is_damaging(self.pz_damage)
            self.damage_player_counter=now
            #深蓝折跃
            self.rect.x +=random.randint(-50, 50)
            self.rect.y +=random.randint(-50,  50)
            self.dx +=12
            self.dy +=12

        for i in list(self.lock.keys()):
            if i not in self.enemyManager.enemies:
                self.lock.pop(i)
        self.platform_create()

    def draw(self):
        if self.trapt:
            #深蓝打击
            for i in self.trapt[:]:
                i["radius"] *=1.02
                u=pygame.draw.circle(self.screen,i["color"],i["pos"],i["radius"],4)
                if u.colliderect(self.player.get_rect()):
                    self.player.is_damaging(damage=5)
                    self.trapt.remove(i)
                    continue
                if i["radius"] >= 75:
                    self.trapt.remove(i)
                    Global.shark_time=6

        w = self.radius if self.radius is not None else self.rect.width
        self.message.font_draw("冰蓝", "", self.screen, self.rect.x + w, self.rect.y -10, self.color)
        self.message.font_draw("HP", f"{self.health:.1f}", self.screen, self.rect.x + w, self.rect.y + 5, self.color)
        extra=(self.damage_time-self.damage_counter) // 1.2
        if self.radius is not None:
            pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y), radius=self.radius)

        b=pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y),self.radius+extra,5)
        #圆环内boss技能: 吸收 冰寒强化自身
        for i in self.enemyManager.enemies:
            if self.circle_collision(b,i.rect) and isinstance(i,IceEnemy):
                if i not in self.lock.keys():
                    self.lock.setdefault(i,0)
                elif self.lock[i]>=200:
                    i.is_alive=False
                    self.health +=2
                    self.damage_counter+=240
                else:
                    self.lock[i]+=1
                    pygame.draw.line(self.screen, i.color, (self.rect.centerx, self.rect.centery),
                                     (i.rect.x, i.rect.y))




    def platform_create(self):
        self.create_platform_counter+=1
        if self.create_platform_counter > self.create_platform_cycle:
            self.platform.boss_exPlatform()
            self.create_platform_counter = 0



    def __del__(self):
        pass