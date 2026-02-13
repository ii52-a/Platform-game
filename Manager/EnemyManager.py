from Manager.EnemyGenerator.Simple_Egenerator import SimpleEGenerator


class EnemyManager:
    def __init__(self, player, screen, traps, platform):
        self.enemies = []
        self.effects=[]
        self.player = player
        self.create_counter = 0
        self.screen = screen
        self.trapManager = traps
        self.platform = platform

        self.generator=SimpleEGenerator(self,self.player,self.screen,self.trapManager,self.platform)

    def update(self):
        self.generator.update()
        # print(Rule.get_stage())
        for p in self.enemies[:]:
            if p.effect:
                self.effects.extend(p.effect)
                p.effect = []
            if not p.is_alive:
                self.enemies.remove(p)
                del p
            else:
                p.update()

        for e in self.effects[:]:
            e.update()
            if not e.is_active:
                self.effects.remove(e)
    def draw(self):
        for i in self.enemies:
            i.draw()
        for e in self.effects:
            e.draw(self.screen)


    def create_enemy(self, ad):
        self.enemies.append(ad)

    def update_generator(self,generator):
        self.generator=generator(self,self.player,self.screen,self.trapManager,self.platform)

    def check_collision(self, player_rect):
        for i in self.enemies:
            if i.rect.colliderect(player_rect):
                i.apply_damage()
