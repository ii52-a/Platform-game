
from loop.rules import Rule
from loop.Config import Config


class Event:
    score = Config.INIT_SCORE

    def __init__(self, screen, player):
        self.time = 0
        self.score_time_get = 0
        self.score_time = 80 - Rule.stage * 5
        self.screen = screen
        self.player = player

    def score_gain(self, score_get):
        self.score_time_get += 1
        if self.score_time_get > self.score_time:
            self.score_time_get = 0
            self.score += score_get * Rule.stage +Config.EXTRA_SCORE
            Rule.stage_change(self.score)

    def game_over(self, health):
        if health <= 0:
            return True
        return None

