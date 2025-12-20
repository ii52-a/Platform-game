import rules


class Event:
    score = 0

    def __init__(self, screen, player):
        self.rule = rules.Rule()
        self.time = 0
        self.score_time_get = 0
        self.score_time = 80 - self.rule.stage * 5
        self.screen = screen
        self.player = player

    def score_gain(self, score_get):
        self.score_time_get += 1
        if self.score_time_get > self.score_time:
            self.score_time_get = 0
            self.score += score_get * self.rule.stage + 150
            self.rule.stage_change(self.score)

    def game_over(self, health):
        if health <= 0:
            return True
        return None

