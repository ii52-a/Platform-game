"""定速块"""
import random

import rules
from PlatForm.platform import Platform


class PlatformKSP(Platform):  #定速定时块
    def __init__(self):
        super().__init__(height=random.randint(30, 25 + 7 * rules.Rule.stage))
        self.speed_x = 3 + 0.1 * rules.Rule.stage
        self.speed_y = 1.2
