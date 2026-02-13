
from loop.rules import Rule
from loop.Config import Config


class Event:
    time = 0
    score_time_get = 0
    score_time = 80 - Rule.stage * 5
    stage_control = None
    screen = None
    player = None
    score=Config.INIT_SCORE

    @classmethod
    def set(cls,screen,stage_control):
        cls.time = 0
        cls.score_time_get = 0
        cls.score_time = 80 - Rule.stage * 5
        cls.stage_control = stage_control
        cls.screen = screen
        cls.score = Config.INIT_SCORE

    @classmethod
    def score_gain(cls, score_get):
        if cls.stage_control.mode!="nexus":
            cls.score_time_get += 1
            if cls.score_time_get > cls.score_time:
                cls.score_time_get = 0
                cls.score += score_get * Rule.stage +Config.EXTRA_SCORE
                Rule.stage_change(cls.score)

    @staticmethod
    def game_over(health):
        if health <= 0:
            return True
        return None

