import pygame

from src.entities.pacman import Pacman
from src.scenes.scene import Scene
from src.utils.enum import Direction
import src.utils.debugger as debugger


class GamePlay(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.pacman = Pacman()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.pacman)

    def render_surface(self):
        self.surface.fill("black")
        self.sprites.draw(self.surface)
        #draw hitbox
        debugger.draw_hitbox(self.surface, self.pacman)

    def handle_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pacman.direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            self.pacman.direction = Direction.RIGHT
        elif keys[pygame.K_UP]:
            self.pacman.direction = Direction.UP
        elif keys[pygame.K_DOWN]:
            self.pacman.direction = Direction.DOWN

    def update(self):
        self.sprites.update()
        self.render_surface()

    def reset(self): pass
