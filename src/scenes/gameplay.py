import pygame

from src.entities.pacman import Pacman
from src.scenes.scene import Scene


class GamePlay(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.pacman = Pacman()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.pacman)

    def render_surface(self):
        self.surface.fill("BLACK")
        self.sprites.draw(self.surface)

    def handle_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pacman.direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.pacman.direction = "right"
        elif keys[pygame.K_UP]:
            self.pacman.direction = "up"
        elif keys[pygame.K_DOWN]:
            self.pacman.direction = "down"

    def update(self):
        self.sprites.update()
        self.render_surface()

    def reset(self): pass
