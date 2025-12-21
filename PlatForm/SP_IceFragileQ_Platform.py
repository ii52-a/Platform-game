
"""疾速破坏冰平台"""
from PlatForm.SP_IceFragile_PlatForm import SPICEPlatform


class SPICEPlatformQ(SPICEPlatform):
    def __init__(self):
        super().__init__((144, 146, 217),(151, 255, 252))
        self.color = (144, 146, 217)
        self.destroy_time= 20


