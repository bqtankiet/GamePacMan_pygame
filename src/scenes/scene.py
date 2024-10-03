import pygame

from src.utils.constant import HEIGHT, WIDTH

class Scene:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.surface.fill("BLACK")
        self.render_surface()
    
    def render(self):
        self.game.screen.blit(self.surface, (0, 0))

    def render_surface(self): pass

    def handle_event(self): pass

    def update(self): pass

    def reset(self): pass
