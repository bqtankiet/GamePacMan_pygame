import pygame

import src.utils.debugger as debugger
from src.entities.ghost import Ghost, GhostRed, RedAIStrategy
from src.entities.maze import Maze, MazeRender
from src.entities.pacman import Pacman
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT
from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader
import src.core.game as g

class GamePlay(Scene):
    """Màn hình Gameplay"""

    def __init__(self):
        super().__init__()
        self._game = g.Game.get_instance()

        self.__maze = Maze(self._game)
        self.__maze_render = MazeRender(self.__maze)
        self._game.game_status.start_game()
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

        pacman = self.__maze.pacman
        if event.key == pygame.K_LEFT:
            pacman.set_next_direction(Direction.LEFT)
        elif event.key == pygame.K_RIGHT:
            pacman.set_next_direction(Direction.RIGHT)
        elif event.key == pygame.K_UP:
            pacman.set_next_direction(Direction.UP)
        elif event.key == pygame.K_DOWN:
            pacman.set_next_direction(Direction.DOWN)
        elif event.key == pygame.K_ESCAPE:
            self._game.game_status.pause()
            self._game.switch_scene("PauseGame")
        elif event.key == pygame.K_p:
            self._game.switch_scene("GameOver")

        # debug
        debugger.handle_event(event)

    def update(self):
        self.__maze.update()

        # Kiểm tra nếu Pacman ăn hết các viên pellet
        if self.__maze.transition_to_next_level:
            self._game.switch_scene("NextLevel")  # Chuyển sang màn kế tiếp hoặc màn hoàn thành

    def reset(self):
        self._game = g.Game.get_instance()
        self.__maze = Maze(self._game)
        self.__maze_render = MazeRender(self.__maze)
        self._game.game_status.start_game()


    def on_enter(self):
        self.__maze.set_state(Maze.READY)
        self._game.game_status.resume()

    #----------------------------------------
    # Các methods riêng của lớp GamePlay
    #----------------------------------------

    def render_status(self):
        self.render_score()
        self.render_highest_score()
        self.render_time()
        self.render_level()
        self.render_lives()

    def render_score(self):
        score = self._game.game_status.current_score()
        score_lbl = ImageLoader().text_image("score")
        score_val = ImageLoader().text_image(f"{score}")
        x = WIDTH // 2 - self.__maze.get_width() // 2 + score_lbl.get_width() // 2
        y = HEIGHT // 2 - self.__maze.get_height() // 2 - score_lbl.get_height() * 2 - 10
        self._surface.blit(score_lbl, score_lbl.get_rect(center=(x, y)))
        self._surface.blit(score_val, score_val.get_rect(center=(x, y + score_lbl.get_height() + 5)))

    def render_highest_score(self):
        highest_score = self._game.game_status.highest_score()
        highest_score_lbl = ImageLoader().text_image("Best Score")
        highest_score_val = ImageLoader().text_image(f"{highest_score}")
        x = WIDTH // 2
        y = HEIGHT // 2 - self.__maze.get_height() // 2 - highest_score_lbl.get_height() * 2 - 10
        self._surface.blit(highest_score_lbl, highest_score_lbl.get_rect(center=(x, y)))
        self._surface.blit(highest_score_val, highest_score_val.get_rect(center=(x, y + highest_score_lbl.get_height() + 5)))

    def render_time(self):
        current_time = self._game.game_status.current_time()
        time_lbl = ImageLoader().text_image("time")
        time_val = ImageLoader().text_image(f"{current_time[0]}'{current_time[1]:02}")
        x = WIDTH // 2 + self.__maze.get_width() // 2 - time_lbl.get_width() // 2
        y = HEIGHT // 2 - self.__maze.get_height() // 2 - time_lbl.get_height() * 2 - 10
        self._surface.blit(time_lbl, time_lbl.get_rect(center=(x, y)))
        self._surface.blit(time_val, time_val.get_rect(center=(x, y + time_lbl.get_height() + 5)))

    def render_level(self):
        level = self._game.game_status.level
        level_lbl = ImageLoader().text_image("level")
        level_val = ImageLoader().text_image(f"{level}")
        x = WIDTH // 2
        y = HEIGHT // 2 + self.__maze.get_height() // 2 + level_lbl.get_height() + 5
        self._surface.blit(level_lbl, level_lbl.get_rect(center=(x, y)))
        self._surface.blit(level_val, level_val.get_rect(center=(x, y + level_lbl.get_height() + 5)))

    def render_lives(self):
        lives = self._game.game_status.lives
        live_img = ImageLoader().pacman_live()
        for i in range(lives):
            x = WIDTH // 2 - self.__maze.get_width() // 2
            y = HEIGHT // 2 + self.__maze.get_height() // 2 + 5
            pos = (x+live_img.get_width()*i, y)
            self._surface.blit(live_img, live_img.get_rect(topleft=pos))