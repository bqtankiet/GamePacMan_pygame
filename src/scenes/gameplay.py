import pygame

from src.entities.maze import Maze
from src.entities.pacman import Pacman
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT
from src.utils.enum import Direction
import src.utils.debugger as debugger


class GamePlay(Scene):
    """Màn hình Gameplay"""

    def __init__(self, game):
        super().__init__(game)
        self.pacman = Pacman()
        self.maze = Maze()
        self.maze.add_pacman(self.pacman, (23 , 14))

    def render_surface(self):
        self.surface.fill("black")
        self.maze.render()
        self.surface.blit(self.maze.surface, self.maze.surface.get_rect(center = (WIDTH//2, HEIGHT//2)))

    def handle_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pacman.next_direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            self.pacman.next_direction = Direction.RIGHT
        elif keys[pygame.K_UP]:
            self.pacman.next_direction = Direction.UP
        elif keys[pygame.K_DOWN]:
            self.pacman.next_direction = Direction.DOWN

    def update(self):
        self.maze.update()
        self.render_surface()

    def reset(self): pass
