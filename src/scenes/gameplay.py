import pygame

from src.entities.maze import Maze
from src.entities.pacman import Pacman
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT
from src.utils.enum import Direction
import src.utils.debugger as debugger


class GamePlay(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.pacman = Pacman()
        self.maze = Maze()
        self.maze.add_pacman(self.pacman, (1 ,1))
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.pacman)

    def render_surface(self):
        self.surface.fill("black")
        self.maze.render()
        self.sprites.draw(self.maze.surface)
        debugger.draw_hitbox(self.maze.surface, self.pacman)
        self.surface.blit(self.maze.surface, self.maze.surface.get_rect(center = (WIDTH//2, HEIGHT//2)))

    def handle_event(self):
        keys = pygame.key.get_pressed()
        next_direction = self.pacman.next_direction
        if keys[pygame.K_LEFT]:
            next_direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            next_direction = Direction.RIGHT
        elif keys[pygame.K_UP]:
            next_direction = Direction.UP
        elif keys[pygame.K_DOWN]:
            next_direction = Direction.DOWN

        self.pacman.next_direction = next_direction

    def update(self):
        self.sprites.update(self.maze)
        self.render_surface()

    def reset(self): pass
