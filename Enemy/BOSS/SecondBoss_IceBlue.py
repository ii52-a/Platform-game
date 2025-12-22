import random

import pygame

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
        self.damage_counter = 180
        self.damage_time =Config.SECONDE_BOSS_INTERNAL
        self.damage_player_counter=0
        self.create_platform_counter=0
        self.create_platform_cycle=80
        self.trapt=[]
        self.first_once=True
        self.dx=0
        self.dy=0
        self.eff=[]


    def update(self):
        rules.Rule.if_boss = True
        rules.Rule.boss_stage = 2
        self.damage_counter += 1
        if self.damage_counter >= self.damage_time:
            self.health -=10
            if self.health >= self.fhealth*3//4:  #第一阶段
                k_num=(self.fhealth-self.health) //10
                for i in range(k_num):
                    #深蓝打击
                    new_trap = {
                        "pos": (random.randint(50, Screen.ScreenX - 50), random.randint(50, Screen.ScreenY - 50)),
                        "radius": 10,
                        "color": (23, 255, 228)
                    }
                    self.trapt.append(new_trap)

            if self.health <= self.fhealth*3//4 and self.first_once:
                for _ in range(5):
                    self.enemyManager.enemies.append([self.create_new_enemy(IceEnemy)])
                #加快施法
                self.damage_counter -=40
                self.first_once=False
            elif self.health >= self.fhealth//2:
                self.dx =random.randint(-8,8)
                self.dy = random.randint(-10,10)
                for _ in range(5):
                    self.trapt.append({
                        "pos": (random.randint(50, Screen.ScreenX - 50), random.randint(50, Screen.ScreenY - 50)),
                            "radius": 5,
                            "color": (4, 148, 131)
                    })
            else:
                self.is_alive=False
            self.damage_counter = 0
        if abs(self.dx)>1 or abs(self.dy)>1:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.dx *=0.92
            self.dy *=0.92
        if self.rect.x-self.radius <=0:
            self.rect.x =self.radius
            self.dx *=-1.2
            self.health -=10
        if self.rect.x+self.radius >= Screen.ScreenX:
            self.rect.x = Screen.ScreenX-self.radius
            self.dx *=-1.2
            self.health -=10
        if self.rect.y+self.radius >= Screen.ScreenY:
            self.rect.y = Screen.ScreenY-self.radius
            self.dy *=-1.2
            self.health -= 10
        if self.rect.y-self.radius <= 0:
            self.rect.y = self.radius
            self.dy *=-1.2
            self.health -= 10
        if self.health <= 0:
            self.is_alive = False
            rules.Rule.if_boss = False
        now=pygame.time.get_ticks()
        if self.rect.colliderect(self.player.get_rect()) and now-self.damage_player_counter>=100:
            self.player.is_damaging(8)
            self.damage_player_counter=now

        a=self.platform.check_collision(self.rect)
        if a:
            a.is_active=False

        self.platform_create()

    def draw(self):
        if self.trapt:
            for i in self.trapt[:]:
                i["radius"]+=2
                u=pygame.draw.circle(self.screen,i["color"],i["pos"],i["radius"])
                if u.collidepoint(self.player.get_rect()):
                    self.player.is_damaging(damage=2)
                    self.trapt.remove(i)
                    continue
                if i["radius"] >= 40:
                    self.trapt.remove(i)
        super().draw()

    def platform_create(self):
        self.create_platform_counter+=1
        if self.create_platform_counter > self.create_platform_cycle:
            self.platform.boss_exPlatform()
            self.create_platform_counter = 0



    def __del__(self):
        pass