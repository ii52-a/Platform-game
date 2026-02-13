from Trap.trap import Trap


class DamageCycle(Trap):
    def update(self):
        pass

    def apply_damage(self):
        pass

    def draw(self, screen):
        pass


    def check_collision(self, player_rect):
        return self.is_active and self.rect.colliderect(player_rect) and player_rect[2]+self.r(player_rect[0]**2-self.x**2)**0.5+(player_rect[1]**2-self.y**2)**0.5