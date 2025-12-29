import math
import random

import pygame

from EffectGlobal import Global
from Effects import CycleDeath
from ..Ice_Enemy import IceEnemy
from Enemy.Basic_Enemy import BasicEnemy
from Manager.PlatFormGenerator import IceBlueGenerator, SimpleGenerator
from loop import rules
from loop.Config import Config, Screen, Show


"""冰蓝"""
class IceBlue(BasicEnemy):
    def __init__(self, screen, player, traps, platform,enemy):
        super().__init__(screen=screen, player=player, traps=traps, platform=platform,enemy=enemy)
        self.fhealth = Config.SECOND_BOSS_HEALTH
        self.health = self.fhealth
        self.color=(0, 10, 103)
        self.radius = 50
        self.rect.x = 640
        self.rect.y = 120

        self.use_sp_platform_generator(IceBlueGenerator)

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
        #连接打断扣血
        self.kc_self_damage=3

        #碰撞玩家扣血
        self.pz_damage=5
        #碰撞冷却
        self.damage_player_counter=0

        #冰圈索敌
        self.ice_lock_player=False
        self.ice_lock_time=0




    def update(self):
        rules.Rule.if_boss = True
        rules.Rule.boss_stage = 2
        self.damage_counter += 1
        if self.health > self.fhealth:
            self.fhealth = self.health
        if self.damage_counter >= self.damage_time:
            self.health -=10
            # 第一阶段
            if self.health >= self.fhealth*3//4:
                k_num=(self.fhealth-self.health) //10
                self.summon_ice(2)

            #切换 过渡技能
            if self.health <= self.fhealth*3//4 and self.first_once:
                self.dx=10
                self.dy=10
                self.summon_ice(3)
                #加快施法-强化
                self.damage_time +=40
                self.create_platform_counter-=10
                self.cz_self_damage =2
                self.first_once=False
                self.kc_self_damage=5
            #第二阶段
            elif self.health >= self.fhealth//2:
                self.color=(0, 28, 111)
                dextra=(self.fhealth-self.health)//5
                self.summon_ice(2)
                self.summon_blue(7)
                self.get_kinetic_energy(dextra,12,6)
            else:
                self.health+=2
                dextra=(self.fhealth-self.health)//10
                self.summon_ice(3)
                self.summon_blue(8)
                self.get_kinetic_energy(dextra,12,6)

            self.damage_counter = 0
        #反弹
        self.put_k_q()
        #死亡
        if self.health <= 0:
            self.is_alive = False
            rules.Rule.if_boss = False
            self._del()
        now=pygame.time.get_ticks()
        if self.check_circle_collision(self.rect,self.radius,self.player.pos,self.player.radius) and now-self.damage_player_counter>=100:
            self.health -=2
            self.damage_player_counter=now
            #深蓝折跃
            self.blue_jump()
        self.apply_ice_pull()

    def draw(self):
        self.draw_blue()

        w = self.radius if self.radius is not None else self.rect.width
        self.message.font_draw("冰蓝", "", self.screen, self.rect.x + w, self.rect.y -10, self.color)
        self.message.font_draw("HP", f"{self.health:.1f}", self.screen, self.rect.x + w, self.rect.y + 5, self.color)
        if self.radius is not None:
            pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y), radius=self.radius)
        if self.ice_lock_player:
            shrink_radius = 200 - self.ice_lock_time
            if shrink_radius > 0:
                pygame.draw.line(self.screen,(36,185,185),(self.rect.x,self.rect.y),self.player.pos,width=shrink_radius//30)
                pygame.draw.circle(self.screen, (36, 185, 185), self.player.pos, shrink_radius, 6)


        self.draw_absorb_ice_line()






    #触墙反弹
    def put_k_q(self):
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
    #深蓝折跃
    def blue_jump(self):
        self.rect.x += random.randint(-50, 50)
        self.rect.y += random.randint(-50, 50)
        self.dx += 15
        self.dy += 15
    #召唤小怪-冰寒
    def summon_ice(self,number):
        for _ in range(number+Show.ICE_BLUE_SUMMON_ADD):
            self.enemyManager.enemies.append(self.create_new_enemy(IceEnemy,if_name=False))

    #深蓝打击！
    def summon_blue(self,number):
        for _ in range(number):
            ax=random.randint(50, Screen.ScreenX - 50)
            bx=random.randint(50, Screen.ScreenX - 50)
            self.trapt.append({
                "pos": (ax,bx),
                "radius": 5,
                "color": (4, 148, 131)
            })
    #装载动能
    def get_kinetic_energy(self,dextra,k1,k2):
        self.dx = random.randint(-k1 - dextra, k1 + dextra)
        self.dy = random.randint(-k2 - dextra, k2 + dextra)

    #冰圈索敌
    def lock_player(self):
        pass

    #拉取冰寒
    def apply_ice_pull(self):
        """冰寒拉取"""
        extra = (self.damage_time - self.damage_counter +(self.fhealth-self.health)//10) // 1.2
        pull_range = self.radius + extra
        if self.check_circle_collision((self.rect.x, self.rect.y), pull_range, self.player.pos, self.player.radius):
            if not self.ice_lock_player:
                self.ice_lock_player=True
            self.ice_lock_time+=2
            dx = self.rect.x - self.player.pos[0]
            dy = self.rect.y - self.player.pos[1]
            self.player.pos[0] += dx * 0.01 + (0.01 if self.health <=self.fhealth//2 else 0)
            self.player.pos[1] += dy * 0.01
            time = 150 - self.ice_lock_time
            if time <= 0:
                self.player.is_damaging(5)
                Global.shark_time = 8
                self.ice_lock_player = False
                self.ice_lock_time = 0

        else:
            self.ice_lock_player=False
            self.ice_lock_time=0

        #吸怪
        for i in self.enemyManager.enemies:
            if isinstance(i, IceEnemy):
                i.boss=None
                if self.check_circle_collision((self.rect.x, self.rect.y), pull_range, i.rect, i.radius):
                    i.boss=self
                    dx = self.rect.x - i.rect.x
                    dy = self.rect.y - i.rect.y
                    dist = math.sqrt(dx ** 2 + dy ** 2)

                    if dist > 2:
                        pull_speed = 1.3 +(0.5*self.damage_counter/self.damage_time)
                        i.rect.x += (dx / dist) * pull_speed
                        i.rect.y += (dy / dist) * pull_speed
                    else:
                        if self.health >= self.fhealth // 2:
                            i.is_alive=False
                            self.effect.append(CycleDeath(self.rect.x, self.rect.y, self.color,max_radius=240,speed=3))
                            self.summon_blue(2)
                            self.damage_counter += 50
                            self.health +=4

    #画-深蓝打击
    def draw_blue(self):
        if self.trapt:
            #深蓝打击
            for i in self.trapt[:]:
                i["radius"] *=1.02
                u=pygame.draw.circle(self.screen,i["color"],i["pos"],i["radius"],4)
                if self.check_circle_collision(i["pos"],i['radius'],self.player.pos,self.player.radius):
                    self.player.is_damaging(damage=3)
                    self.trapt.remove(i)
                    continue
                if i["radius"] >= 75:
                    self.trapt.remove(i)
                    Global.shark_time=6
    #画-吸收牵引线
    def draw_absorb_ice_line(self):

        extra = (self.damage_time - self.damage_counter+(self.fhealth-self.health)//10) // 1.2
        pull_range = self.radius + extra
        pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y), pull_range, 5)

        for i in self.enemyManager.enemies:
            if isinstance(i, IceEnemy):
                if self.check_circle_collision((self.rect.x, self.rect.y), pull_range, i.rect, i.radius):
                    pygame.draw.line(self.screen, i.color, (self.rect.x, self.rect.y),
                                     (i.rect.x, i.rect.y), 1)

    def link_self_damage(self):
        self.health-=self.kc_self_damage
        self.damage_counter -= 20
    def _del(self):
        self.use_sp_platform_generator(SimpleGenerator)
        rules.Rule.if_boss=False