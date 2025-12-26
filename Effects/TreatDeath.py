from loop import message

"""治疗信息 HP+10"""
class TreatDeath:
    def __init__(self, x, y,color=(79, 221, 60)):
        self.x = x
        self.y = y
        self.color = color
        self.font_size=42
        self.min_font_size=6
        self.dy=2
        self.is_active = True
        self.speed = 1
        self.message= message.Message()

    def update(self):
        self.font_size-=self.speed
        self.y-=self.dy
        if self.font_size < self.min_font_size:
            self.is_active = False

    def draw(self, screen):
        if self.is_active:
            self.message.font_draw("HP","+10",screen, self.x, self.y, self.color)
