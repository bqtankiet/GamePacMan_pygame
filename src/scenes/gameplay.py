import pygame

from src.entities.ghost import Ghost
from src.entities.maze import Maze, MazeRender
from src.entities.pacman import Pacman
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT
from src.utils.enum import Direction


class GamePlay(Scene):
    """Màn hình Gameplay"""

    def __init__(self, game):
        super().__init__(game)
        self.__pacman = Pacman()
        self.__ghost = Ghost()

        self.__maze = Maze()
        self.__maze.add_entity(self.__ghost, (1, 1))
        self.__maze.add_entity(self.__pacman, (23, 14))
        self.__maze_render = MazeRender(self.__maze)

    #-----------------------------------------
    # Các methods override của lớp cha (Scene)
    #-----------------------------------------
    def render_surface(self):
        maze_surface = self.__maze_render.render()
        maze_rect = maze_surface.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self._surface.blit(maze_surface, maze_rect)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN: return

        if event.key == pygame.K_LEFT:
            self.__pacman.set_next_direction(Direction.LEFT)
        elif event.key == pygame.K_RIGHT:
            self.__pacman.set_next_direction(Direction.RIGHT)
        elif event.key == pygame.K_UP:
            self.__pacman.set_next_direction(Direction.UP)
        elif event.key == pygame.K_DOWN:
            self.__pacman.set_next_direction(Direction.DOWN)
        elif event.key == pygame.K_ESCAPE:
            self._game.switch_scene("PauseGame")
        elif event.key == pygame.K_p:
            self._game.switch_scene("GameOver")

    def update(self):
        self.__maze.update()
        self.render_surface()

    def reset(self):
        pass

    #----------------------------------------
    # Các methods riêng của lớp GamePlay
    #----------------------------------------
