import math

import pygame.draw

from EffectGlobal import Global
from loop.Config import Screen, Show
from loop.message import Message


class RecallWorld:
    def __init__(self, screen):
        self.screen = screen

        #中心轴点
        self.mid=pygame.Vector2(int(Screen.ScreenX/2),0)
        self.horizon_top=200

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

        #树叶视角感
        self.tree_radius_add=12

        #视野摄像模拟
        self.view_offset = 0
        self.camera_z = 0
        self.camera_x = 0

        self.message=Message()
        self.recall_counter=0 if not Show.SKIP_NEX else 1840
        self.is_recalling=False


        self.cycle1=pygame.Vector2(500,500)
        self.cycle1_depth=0.5
        self.cycle2=pygame.Vector2(700,500)
        self.cycle2_depth=0.5
        self.cycle2_radius=0
        self.cycle1_message=""
        self.cycle2_message=""

    #深度，是用来处理左右看时远近变化的不同，远处深度应该更大，变化更小
    #侧偏移，用来控制摆头角度，即增加的横向向量长度

    #comera_z本质是改变 树的插值间隔来模拟前进

    #view——offset是侧偏移量
    #comera_x本质就是转动视角 !只是视角太大了,远处和近处移动都很大，使得出现移动的错觉
    """以上都是错误理解，无法进行彻底的转头，正确的伪3d应该是固定物体，移动视角，而不是移动画布"""

    def update(self):
        #region
        keys = pygame.key.get_pressed()
        #前进
        if keys[pygame.K_w]:
            if self.road_degree<=800:
                self.camera_z-=0.01
            if self.tree_radius_add>=7:
                self.tree_radius_add-=0.02
        #后退
        elif keys[pygame.K_s]:
            if self.road_degree>=20:
                self.road_degree-=0.02
                self.camera_z+=0.01
            if self.tree_radius_add<12:
                self.tree_radius_add+=0.02
        #向左
        if keys[pygame.K_a]:
            self.camera_x+=1
        #向右
        elif keys[pygame.K_d]:
            self.camera_x-=1
        #左转头
        if keys[pygame.K_q]:
            self.view_offset += 3
            # self.horizon_top +=1
        #右转头
        elif keys[pygame.K_e]:
            self.view_offset -= 3
            # self.horizon_top -= 1
        self._update()
        self.draw()
        #endregion
        self.recall_counter+=1
        if self.recall_counter >= 100:
            self.is_recalling=True
            self.camera_z-=0.003
            if self.recall_counter <=200:
                self.cycle1_message="..."
            elif self.recall_counter <=400:
                self.cycle2_message="....."
            elif self.recall_counter <=700:
                self.cycle1_message="..."
            elif self.recall_counter <=1000:
                self.cycle2-=pygame.Vector2(0,0.01)
                self.cycle1_depth-=0.0005
                self.cycle2_depth-=0.001
            elif self.recall_counter <=1260:
                self.cycle2_message="..,....."
            elif self.recall_counter <=1440:
                self.cycle2 -= pygame.Vector2(0, 0.01)
                self.cycle1_depth-=0.0005
                self.cycle2_depth-=0.001
                self.cycle1_message="..............。"
            elif self.recall_counter<=1840:
                self.cycle1_depth-=0.0005
                self.cycle2_depth-=0.001
            else:
                Global.is_recall=False


    def _update(self):
        # 路向量长
        self.road_length = pygame.Vector2(0, int((Screen.ScreenY - self.horizon_top) / math.cos(
            math.radians(self.road_degree))))

        # self.road_length_left=pygame.Vector2(0,min(self.road_length.y,int(self.mid_left.x / math.sin(math.radians(self.road_degree)))))
        # self.road_length_right=pygame.Vector2(0,min(self.road_length.y,int((Screen.ScreenX -self.mid_right.x) / math.sin(math.radians(self.road_degree)))))
        self.road_length_left=self.road_length
        self.road_length_right=self.road_length

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
        #模拟深度
        mid_depth = 0.9
        road_depth = 0.1
        self.p_mid_left = self.apply_view_offset(self.mid_left, mid_depth)
        self.p_mid_right = self.apply_view_offset(self.mid_right, mid_depth)
        self.p_road_left = self.apply_view_offset(self.road_left, road_depth)
        self.p_road_right = self.apply_view_offset(self.road_right, road_depth)

        road_rect_points = [
            self.p_road_left,
            self.p_road_right,
            self.p_mid_right,
            self.p_mid_left,
        ]
        bottom_depth = 0.05
        p_bottom_left = self.apply_view_offset(pygame.Vector2(0, Screen.ScreenY), bottom_depth)
        p_bottom_right = self.apply_view_offset(pygame.Vector2(Screen.ScreenX, Screen.ScreenY), bottom_depth)
        road_rect_fill_points = [
            self.p_road_left,
            self.p_road_right,
            p_bottom_right,
            p_bottom_left,
        ]

        grass_points=[
            (0,self.horizon_top),
            (Screen.ScreenX, self.horizon_top),
            (Screen.ScreenX, Screen.ScreenY),
            (0,Screen.ScreenY),
        ]

        #road路
        pygame.draw.line(self.screen, (0, 0, 0), self.p_mid_left, self.p_road_left, 1)
        pygame.draw.line(self.screen, (0, 0, 0), self.p_mid_right, self.p_road_right, 1)
        pygame.draw.polygon(self.screen, (100, 100, 100), grass_points)

        pygame.draw.polygon(self.screen, (210, 130, 80), sky_rect_points)
        pygame.draw.polygon(self.screen, (60, 60, 65), road_rect_points)
        pygame.draw.polygon(self.screen, (60, 60, 65), road_rect_fill_points)




        #horizon地平线
        pygame.draw.line(self.screen,(0,0,0),(0,self.horizon_top),(Screen.ScreenX,self.horizon_top),1)

        #树
        #延迟渲染避免透视
        draw_tree=[]
        for i in range(5):
            z_raw = (i*2 - self.camera_z) % 10
            d_length= 10 +15*z_raw**1.7
            depth=math.pow(z_raw / 10, 2)
            p1=self.p_mid_left.lerp(self.p_road_left,depth)
            p2=self.p_mid_right.lerp(self.p_road_right,depth)
            dy=pygame.Vector2(0,-d_length)
            draw_tree.append((z_raw,p1,p2,dy))

        draw_tree.sort(key=lambda x:x[0],reverse=False)

        #渲染人物
        if self.is_recalling:
            if self.cycle1_depth>0 and self.cycle2_depth>0:
                c1 = self.p_mid_left.lerp(self.p_road_left, self.cycle1_depth)
                c2 = self.p_mid_right.lerp(self.p_road_right, self.cycle2_depth)
                cycle2 = c1.lerp(c2, max(0.95 - self.cycle2_depth / 2, 0.1))
                cycle1 = c1.lerp(c2, max(0.55 - self.cycle1_depth / 2, 0.1))
                pygame.draw.circle(self.screen, (0, 0, 0), cycle1, 40*(self.cycle1_depth-0.1))
                pygame.draw.circle(self.screen, (0, 0, 0), cycle2, self.cycle2_radius+60*self.cycle2_depth)
            else:
                self.is_recalling=False
        #渲染
        for i in draw_tree:
            pygame.draw.line(self.screen, (0, 0, 0), i[1], i[1] + i[3], int(2 + i[0]))
            pygame.draw.line(self.screen, (0, 0, 0), i[2], i[2] + i[3], int(2 + i[0]))
            pygame.draw.circle(self.screen,(17, 94, 0),i[1]+i[3],i[0]*5)
            pygame.draw.circle(self.screen,(17, 94, 0),i[2]+i[3],i[0]*5)
        if self.cycle1_message and self.is_recalling:
            self.message.font_draw(self.cycle1_message,"",self.screen,cycle1.x,cycle1.y-70,(0,0,0),32)
        if self.cycle2_message and self.is_recalling:
            self.message.font_draw(self.cycle2_message,"",self.screen,cycle2.x,cycle2.y-self.cycle2_radius-20,(0,0,0),32)



        self.message.font_draw("无法回忆的公路","",self.screen,10,10,(0,0,0),24)


    def apply_view_offset(self, point, depth):
        # 应用深度
        """
        mid_depth = 2
        road_depth = 18
        self.p_mid_left = self.apply_view_offset(self.mid_left, mid_depth)
        self.p_mid_right = self.apply_view_offset(self.mid_right, mid_depth)
        self.p_road_left = self.apply_view_offset(self.road_left, road_depth)
        self.p_road_right = self.apply_view_offset(self.road_right, road_depth)
        """
        ddepth=1-depth
        return point + pygame.Vector2(self.view_offset, 0) + pygame.Vector2(self.camera_x * ddepth*10, 0)











