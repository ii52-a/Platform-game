import math
import random

import pygame

from EffectGlobal import Global
from Effects import CycleDeath
from Effects.LineEffect import LightningEffect
from loop.Config import Screen, Show
from loop.message import Message


class TalkerFriend:
    def __init__(self,screen,player,name,color,bottom,leg_length=40,body_length=10,neck_length=20,arm_length=30,head_radius=20,arm_degree=45,leg_degree=30):




        self.name = name
        self.player = player
        self.color = color
        self.screen = screen
        #底部中心 坐标
        self.bottom=pygame.Vector2(bottom[0],bottom[1])
        self.rect = pygame.Rect(0, 0, 1, 1)

        self.leg_length = leg_length
        self.arm_length = arm_length
        self.neck_length = neck_length
        self.body_length = body_length


        self.leg_degree = leg_degree
        self.arm_l_degree = arm_degree
        self.arm_r_degree = arm_degree
        self.head_radius = head_radius
        self.effect=None
        self.is_alive = True

        self.arm_setting=True
        self.message=Message()
        self.stage=0

        #玩家动量  向量动量
        self.pump = 0
        #向左动量
        self.l_pump =0

        self.effect_counter=0
        self.talk_counter=0
        self.effect=[]

        self.talk_list=[
            "你说意识是什么？",
            "我为什么在这里？",
            "你在想，或许没有人是存在的。",
            "你应该明白了，然后\"醒来\"。",
            "我比你厉害多了,不信你看..可我还是止步不前。",
            "或许平凡也能快乐。你甘于此吗？",
            "意识受物质牵制，没人定义它。",
            "你怎么确定自洽系统没有意识？过来伙计。",
            "别问我为什么这么简陋，你可只是个球。",
            "总有一天，\"你会让我更完善的。\"",
            "怎么确定？什么逻辑？",
            "别紧张，只是跟你开个玩笑。准备好了吗？",
            "我跟你讲个故事吧。"
        ]
        self.talk_z=0 if not Show.SKIP_NEX else 12
        self.tz_add = 0
        self.talk_message="?"
        self.vel_talk_message="..."
        self.is_talking=False
        self.talk_interval=20
        self.once=[True,True,True]
        #特殊状态设置 [player_lock,动画]
        self.tz11_once=[True,True]
        self.tz11_counter=0
        self.tz12_counter=0 if not Show.SKIP_NEX else 1800
        self.tz12_once=[True]
        self.tz_end = 0
    def _update_body(self):
        if self.talk_z==7:
            if self.arm_setting:
                self.arm_r_degree +=1
                if self.arm_r_degree >=70:
                    self.arm_setting = False
            elif not self.arm_setting:
                self.arm_r_degree -= 1
                if self.arm_r_degree <=30:
                    self.arm_setting = True
        self.leg_start=pygame.Vector2(0, -self.leg_length*math.cos(math.radians(self.leg_degree)))+self.bottom

        self.leg_e=pygame.Vector2(0, self.leg_length)

        self.leg_end_l=self.leg_start+self.leg_e.rotate(self.leg_degree)
        self.leg_end_r=self.leg_start+self.leg_e.rotate(-self.leg_degree)

        self.body_e=pygame.Vector2(0, -self.body_length)
        self.neck_e=pygame.Vector2(0, -self.neck_length)

        #脖子
        self.neck_start=self.leg_start+self.body_e
        self.neck_end=self.neck_start+self.neck_e


        self.arm_start=self.neck_start
        self.arm_e=pygame.Vector2(0, -self.arm_length)
        self.arm_end_l=self.neck_start+self.arm_e.rotate(-self.arm_l_degree)
        self.arm_end_r=self.neck_start+self.arm_e.rotate(self.arm_r_degree)

        #头
        self.head_e=pygame.Vector2(0, -self.head_radius)
        self.head_start=self.neck_end+self.head_e








    def update(self):

        self.update_effects()

        self.pump_player()
        self.left_pump_player()

        self.check_collision()

        self.talk_main()

        if self.stage==1:
            self._update_body()
    def update_effects(self):
        self.effect_counter += 1
        for i in self.effect[:]:
            i.update()
            if not i.is_active:
                self.effect.remove(i)

    def talk_main(self):
        if self.is_talking:
            self.talk_message = self.talk_list[self.talk_z]
            # tz4
            if self.talk_z == 4 and self.once[0]:
                self.tz4()
            # tz7
            if self.talk_z == 7 and self.once[1]:
                self.tz7()
            # tz11
            if self.talk_z == 11 and self.once[2]:
                self.tz11()
            # tz12
            if self.talk_z == 12:
                self.tz12()
            self.talk_counter += 1


            #短暂回忆
            if self.talk_z > 0:
                self.vel_talk_message = self.talk_list[self.talk_z - 1]


            #单次谈话冷却和更替
            if self.talk_counter >= self.talk_interval:
                if self.talk_z + 1 < len(self.talk_list):
                    self.talk_z += 1
                self.is_talking = False
                self.talk_counter = 0
            # 短暂回忆

    def pump_player(self):
        if abs(self.pump)>1:
            dx=self.player.pos[0]-self.bottom.x
            dy=self.player.pos[1]-self.bottom.y
            d=math.sqrt(dx**2+dy**2)
            tdx = (dx/d)*self.pump
            tdy = (dy/d)*self.pump
            self.player.be_moved(tdx,tdy)
            self.pump *=0.86

    def left_pump_player(self):
        if self.l_pump>1:
            self.player.be_moved(-self.l_pump*0.86,0)
            self.l_pump *=0.86


    def check_collision(self):
        if self.check_circle_collision((self.bottom.x, self.bottom.y - self.head_radius), self.head_radius,
                                       (self.player.pos[0], self.player.pos[1]), self.player.radius):
            self.pump=100

        if self.stage==0 and not self.is_talking:
            if self.check_circle_collision((self.bottom.x, self.bottom.y - self.head_radius), self.head_radius + 70,
                                           (self.player.pos[0], self.player.pos[1]), self.player.radius):
                self.is_talking = True

        elif self.stage==1 and not self.is_talking:
            if self.check_circle_collision((self.bottom.x, self.bottom.y - self.body_length-self.leg_length), self.head_radius +70+self.tz_add,
                                           (self.player.pos[0], self.player.pos[1]), self.player.radius):
                self.is_talking = True

    def tz4(self):
        self.once[0] = False
        for _ in range(5):
            pos = (random.randint(10, Screen.ScreenX - 10), random.randint(10, Screen.ScreenY - 10))
            self.effect.append(
                LightningEffect((self.bottom.x, self.bottom.y - self.head_radius), pos, duration=120,
                                color=self.color))

    def tz7(self):
        self.once[1] = False
        self.stage = 1
        self.pump = 200
        self.talk_interval += 20

    def tz11(self):
        if self.tz11_once[0]:
            self.lock_player()
            self.tz11_once[0]=False
        #持续控制位置
        self.player.pos[0] = self.arm_end_r.x
        self.player.pos[1] = self.arm_end_r.y
        if self.arm_r_degree<=70 and self.tz11_once[1]:
            self.arm_r_degree+=0.5
            self.leg_degree +=0.5
        if self.arm_r_degree >=70 and self.tz11_once[1]:
            self.tz11_once[1]=False

        if self.arm_r_degree>=20 and not self.tz11_once[1]:
            self.arm_r_degree-=0.5
            self.arm_l_degree+=0.5
        if self.arm_r_degree <=20:
            self.delock_player()
            self.once[2]=False
            self.talk_z+=1

    def tz12(self):
        self.tz12_counter+=1
        self.tz_add=500
        if self.tz12_counter<=180:
            self.talk_message="我想起来了。"
        elif self.tz12_counter<=340:
            self.talk_message="其实我就是你。"
        elif self.tz12_counter<=500:
            self.talk_message="我停下了，或许我恐惧了，或许我失败了"
        elif self.tz12_counter<=640:
            self.talk_message="你呢？你为什么不恐惧？"
        elif self.tz12_counter<=1420:
            if self.tz12_once[0]:
                self.lock_player()
                self.tz12_once[0] = False
            if self.tz12_counter<=800:
                self.player.pos[0] = self.arm_end_r.x
                self.player.pos[1] = self.arm_end_r.y
                self.leg_length+=0.1
                self.arm_length-=0.11
                self.talk_message="我不想“我”再放弃了。"
            elif self.tz12_counter<=1000:
                self.player.pos[0] = self.arm_end_r.x
                self.player.pos[1] = self.arm_end_r.y
                self.arm_r_degree -= 0.15
                Global.shark_time =3
                self.talk_message="你还记得那个意气风发的你吗？"
            elif self.tz12_counter<=1420:
                Global.shark_time =2
                if self.tz12_counter>=1300:
                    Global.shark_time = 6
                self.player.pos[0] = self.head_start.x
                self.player.pos[1] = self.head_start.y
                self.talk_message="想起来吧。"

        elif self.tz12_counter<=1800:
            self.player.pos[0] = self.head_start.x
            self.player.pos[1] = self.head_start.y
            Global.shark_time = 3
            self.tz_end+=1
        else:
            Global.is_recall=1
            self.is_alive=False
            if not  Show.SKIP_NEX:
                self.delock_player()




    def lock_player(self):
        self.f_interval = self.talk_interval
        self.f_speed = self.player.speed
        self.fhv = self.player.jump_speedMax
        self.f_leg_degree = self.leg_degree
        self.f_l_arm_degree = self.arm_l_degree
        self.f_r_arm_degree = self.arm_r_degree
        self.talk_interval = 9999
        self.player.jump_speedMax = 0
        self.player.is_downJumping = True
        if self.player.current_platform:
            self.player.leave_platform()
        self.player.speed = 0
        self.arm_length *= 1.5

    def delock_player(self):
        self.l_pump = 200
        self.player.speed = self.f_speed
        self.player.jump_speedMax = self.fhv
        self.player.is_downJumping = False
        self.talk_interval = self.f_interval
        self.leg_degree = self.f_leg_degree
        self.arm_l_degree = self.f_l_arm_degree
        self.arm_r_degree = self.f_r_arm_degree
    def draw(self):
        #特效
        for i in self.effect:
            i.draw(self.screen)

        #球形态
        if self.stage==0:
            if self.effect_counter>=100:
                self.effect.append(CycleDeath(self.bottom.x,self.bottom.y-self.head_radius,color=(255,255,255)))
                self.effect_counter=0
            pygame.draw.circle(self.screen, (175, 175, 175), (self.bottom.x,self.bottom.y-self.head_radius), self.head_radius)
            self.message.font_draw(self.name, "", self.screen, self.bottom.x, self.bottom.y - self.head_radius - 10)
            self.message.font_draw(self.talk_message, "", self.screen, self.bottom.x, self.bottom.y - self.head_radius - 50)
            if self.talk_z>0:
                self.message.font_draw(self.vel_talk_message, "", self.screen, self.bottom.x,
                                       self.bottom.y - self.head_radius - 80,font_size=12)
        #火柴人形态
        elif self.stage==1:
            pygame.draw.circle(self.screen,self.color,self.head_start,self.head_radius)
            pygame.draw.line(self.screen,self.color,self.arm_start,self.arm_end_l)
            pygame.draw.line(self.screen,self.color,self.arm_start,self.arm_end_r)
            pygame.draw.line(self.screen,self.color,self.leg_start,self.leg_end_l)
            pygame.draw.line(self.screen,self.color,self.leg_start,self.leg_end_r)
            pygame.draw.line(self.screen,self.color,self.leg_start,self.neck_start)
            pygame.draw.line(self.screen,self.color,self.neck_start,self.neck_end)
            self.message.font_draw(self.name, "", self.screen, self.bottom.x, self.bottom.y - self.head_radius - 10)
            self.message.font_draw(self.talk_message,"",self.screen,self.bottom.x,self.head_start.y-self.head_radius-20)
        if self.tz_end:
            pygame.draw.circle(self.screen,(255,255,255),(Screen.ScreenX//2,Screen.ScreenY//2),self.tz_end)


    @staticmethod
    def check_circle_collision(pos1, radius1, pos2, radius2):
        """
        pos1: 第一个圆的中心点 (x, y)
        radius1: 第一个圆的半径
        pos2: 第二个圆的中心点 (x, y)
        radius2: 第二个圆的半径
        """
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance <= (radius1 + radius2)


