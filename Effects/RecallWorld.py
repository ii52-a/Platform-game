import math

import pygame.draw

from loop.Config import Screen


class RecallWorld:
    def __init__(self, screen):
        self.screen = screen

        #中心轴点
        self.mid=pygame.Vector2(int(Screen.ScreenX/2),0)
        self.horizon_top=50

        #路的偏斜角
        self.road_degree=50
        #路向量长
        self.road_length=pygame.Vector2(0,int((Screen.ScreenY-self.horizon_top) / math.cos(math.radians(self.road_degree))))
        self.road_left=self.road_length.rotate(self.road_degree)
        self.road_right=self.road_length.rotate(-self.road_degree)

        #左右路偏移
        self.mid_py=pygame.Vector2(10,0)
        #地平线向量
        self.horizon_py=pygame.Vector2(0,self.horizon_top)

        #中心差向量
        self.mid_left=self.mid-self.mid_py+self.horizon_py
        self.mid_right=self.mid+self.mid_py+self.horizon_py

        #路
        self.road_left=self.road_left+self.mid_left
        self.road_right=self.road_right+self.mid_right

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.road_degree-=0.1
        elif keys[pygame.K_s]:
            self.road_degree+=0.1
        self._update()
        self.draw()

    def _update(self):
        # 路向量长
        self.road_length = pygame.Vector2(0, int((Screen.ScreenY - self.horizon_top) / math.cos(
            math.radians(self.road_degree))))

        self.road_length_left=pygame.Vector2(0,min(self.road_length.y,int(self.mid_left.x / math.sin(math.radians(self.road_degree)))))
        self.road_length_right=pygame.Vector2(0,min(self.road_length.y,int((Screen.ScreenX -self.mid_right.x) / math.sin(math.radians(self.road_degree)))))
        self.road_left = self.road_length_left.rotate(self.road_degree)
        self.road_right = self.road_length_right.rotate(-self.road_degree)

        # 左右路偏移
        self.mid_py = pygame.Vector2(10, 0)
        # 地平线向量
        self.horizon_py = pygame.Vector2(0, self.horizon_top)

        # 中心差向量
        self.mid_left = self.mid - self.mid_py + self.horizon_py
        self.mid_right = self.mid + self.mid_py + self.horizon_py

        # 路
        self.road_left = self.road_left + self.mid_left
        self.road_right = self.road_right + self.mid_right

    def draw(self):
        sky_rect_points = [
            (0, 0),
            (Screen.ScreenX, 0),
            (Screen.ScreenX, self.horizon_top),
            (0, self.horizon_top)
        ]
        road_rect_points = [
            (self.road_left.x, self.road_left.y),
            (self.road_right.x, self.road_right.y),
            (self.mid_right.x, self.mid_right.y),
            (self.mid_left.x, self.mid_left.y),
        ]

        road_rect_fill_points = [
            (self.road_left.x, self.road_left.y),
            (self.road_right.x, self.road_right.y),
            (Screen.ScreenX, Screen.ScreenY),
            (0,Screen.ScreenY),
        ]
        grass_points=[
            (0,self.horizon_top),
            (Screen.ScreenX, self.horizon_top),
            (Screen.ScreenX, Screen.ScreenY),
            (0,Screen.ScreenY),
        ]
        # grass_left_points = [
        #     (0,self.horizon_top),
        #     (self.mid_left.x, self.horizon_top),
        #     (0,self.road_left.y),
        # ]
        # grass_right_points = [
        #     (self.mid_right.x, self.horizon_top),
        #     (Screen.ScreenX, self.horizon_top),
        #     (Screen.ScreenX, self.road_right.y),
        # ]


        pygame.draw.polygon(self.screen, (100, 100, 100), grass_points)

        pygame.draw.polygon(self.screen, (210, 130, 80), sky_rect_points)
        pygame.draw.polygon(self.screen, (60, 60, 65), road_rect_points)
        pygame.draw.polygon(self.screen, (60, 60, 65), road_rect_fill_points)

        # pygame.draw.polygon(self.screen, (100, 100, 100), grass_left_points)
        # pygame.draw.polygon(self.screen, (100, 100, 100), grass_right_points)



        #horizon地平线
        pygame.draw.line(self.screen,(0,0,0),(0,self.horizon_top),(Screen.ScreenX,self.horizon_top),1)
        # pygame.draw.line(self.screen,(0,0,0),(self.mid_right.x,self.horizon_top),(Screen.ScreenX,self.horizon_top),1)
        for i in range(5):
            di=((i+1) / 6)**2

            d_length= 20 +15*i**2
            p1=self.mid_left.lerp(self.road_left,di)
            p2=self.mid_right.lerp(self.road_right,di)

            dy=pygame.Vector2(0,-d_length)

            pygame.draw.line(self.screen,(0,0,0),p1,p1+dy,2+i)
            pygame.draw.line(self.screen,(0,0,0),p2,p2+dy,2+i)
            tree_ly=p1+dy
            tree_ry=p2+dy
            pygame.draw.circle(self.screen,(17, 94, 0),tree_ly,12+i*10)
            pygame.draw.circle(self.screen,(17, 94, 0),tree_ry,12+i*10)
            rect_points = [

            ]





        #road路
        pygame.draw.line(self.screen,(0,0,0),self.mid_left,self.road_left,1)
        pygame.draw.line(self.screen,(0,0,0),self.mid_right,self.road_right,1)




