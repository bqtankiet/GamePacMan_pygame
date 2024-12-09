import pygame

import src.utils.debugger as debugger
from src.entities.ghost import Ghost, GhostRed, RedAIStrategy
from src.entities.maze import Maze, MazeRender
from src.entities.pacman import Pacman
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT
from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader

class GamePlay(Scene):
    """Màn hình Gameplay"""

    def __init__(self, game):
        super().__init__(game)
        self.__pacman = Pacman()
        self.__ghost = GhostRed()

        self.__maze = Maze(game)
        self.__maze.add_entity(self.__ghost, RedAIStrategy.SPAWN_POS)
        self.__maze.add_entity(self.__pacman, (23, 14))
        self.__maze_render = MazeRender(self.__maze)
        self._game.game_status.start = pygame.time.get_ticks()
        self._game.game_status.score = 0
    #-----------------------------------------
    # Các methods override của lớp cha (Scene)
    #-----------------------------------------
    def render_surface(self):
        self._surface.fill((0, 0, 0))
        maze_surface = self.__maze_render.render()
        maze_rect = maze_surface.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self._surface.blit(maze_surface, maze_rect)
        self.render_status()

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

        # debug
        debugger.handle_event(event)

    def update(self):
        self.__maze.update()
        self.render_surface()

    def reset(self):
        self.__maze.set_state(Maze.READY)

    #----------------------------------------
    # Các methods riêng của lớp GamePlay
    #----------------------------------------

    def render_status(self):
        ### Score
        score = self._game.game_status.current_score()
        score_lbl = ImageLoader().text_image("score")
        score_val = ImageLoader().text_image(f"{score}")
        x = WIDTH//2 - self.__maze.get_width()//2 + score_lbl.get_width()//2
        y = HEIGHT//2 - self.__maze.get_height()//2 - score_lbl.get_height()*2 - 10
        self._surface.blit(score_lbl, score_lbl.get_rect(center = (x, y)))
        self._surface.blit(score_val, score_val.get_rect(center = (x, y+score_lbl.get_height()+5)))

        ### Highest Score
        highest_score = self._game.game_status.highest_score()
        highest_score_lbl = ImageLoader().text_image("Best Score")
        highest_score_val = ImageLoader().text_image(f"{highest_score}")
        x = WIDTH//2
        y = HEIGHT//2 - self.__maze.get_height()//2 - highest_score_lbl.get_height()*2 - 10
        self._surface.blit(highest_score_lbl, highest_score_lbl.get_rect(center = (x, y)))
        self._surface.blit(highest_score_val, highest_score_val.get_rect(center = (x, y+highest_score_lbl.get_height()+5)))

        ### Time
        current_time = self._game.game_status.current_time()
        time_lbl = ImageLoader().text_image("time")
        time_val = ImageLoader().text_image(f"{current_time[0]}'{current_time[1]:02}")
        x = WIDTH//2 + self.__maze.get_width()//2 - time_lbl.get_width()//2
        y = HEIGHT//2 - self.__maze.get_height()//2 - time_lbl.get_height()*2 - 10
        self._surface.blit(time_lbl, time_lbl.get_rect(center = (x, y)))
        self._surface.blit(time_val, time_val.get_rect(center = (x, y+time_lbl.get_height()+5)))