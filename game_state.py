class GameState:
    def __init__(self):
        self.score = 0
        self.game_over = False

    def update(self, player, dt):
        player.regenerate_health(dt)
        if player.health <= 0:
            self.set_game_over()

    def increment_score(self, points):
        self.score += points

    def is_game_over(self):
        return self.game_over

    def set_game_over(self):
        self.game_over = True

    def reset(self):
        self.score = 0
        self.game_over = False