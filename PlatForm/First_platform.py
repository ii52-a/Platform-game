#初始平台
from PlatForm.platform import Platform


class PlatformFirst(Platform):
    def __init__(self, player_pos, width=250, height=30, color=(0, 75, 0)):
        # 计算平台位置：玩家脚下
        x = player_pos[0] - width // 2  # 玩家位置居中
        y = player_pos[1] + 20  # 玩家半径下方
        self.pos = (x, y)
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        # 初始不移动
        self.speed_x = 0
        self.speed_y = 0
        self.is_gaming = False

    def update(self):
        # print(self.is_gaming)
        if self.is_gaming:
            self.speed_x = 1
            self.speed_y = 1
        super().update()

