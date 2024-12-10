import sys

import pygame

import src.utils.constant as const
from src.scenes.game_over import GameOver
import src.scenes.gameplay as gp
from src.scenes.main_menu import MainMenu
from src.scenes.pause_game import PauseGame


class Game:
    def __init__(self):
        # init pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('PacMan')

        # init attributes
        self.game_status = GameStatus(self)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT), pygame.FULLSCREEN)
        self.scenes = {
            "MainMenu": MainMenu(self),
            "GamePlay": gp.GamePlay(self),
            "GameOver": GameOver(self),
            "PauseGame": PauseGame(self),
            # other screens go here
        }
        self.current_scene = self.scenes["MainMenu"]
        self.running = True

    def switch_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.reset()  # Đặt lại màn hình mới

    def run(self):
        """Game loop chính"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.render()

            pygame.display.flip()
            self.clock.tick(const.FPS)
        pygame.quit()
        sys.exit()

    def exit(self):
        self.running = False

    def new_game(self):
        self.scenes["GamePlay"] = gp.GamePlay(self)



class GameStatus:
    SCORE_PELLET = 10
    SCORE_POWER_PELLET = 100
    SCORE_GHOST = 200

    def __init__(self, game):
        self.game = game
        self.score = 0
        self.start = 0
        self.best_score = 0
        self.total_pause_duration = 0
        self.pause_start = None
        self.lives = 3
        self.level = 1

    def start_game(self):
        self.start = pygame.time.get_ticks()
        self.total_pause_duration = 0
        self.score = 0
        self.pause_start = None

    def pause(self):
        if self.pause_start is None:
            self.pause_start = pygame.time.get_ticks()

    def resume(self):
        if self.pause_start is not None:
            self.total_pause_duration += pygame.time.get_ticks() - self.pause_start
            self.pause_start = None

    def current_time(self):
        if self.start == 0:
            return 0, 0

        elapsed_time = pygame.time.get_ticks() - self.start - self.total_pause_duration

        total_secs = elapsed_time // 1000
        minutes = total_secs // 60
        seconds = total_secs % 60
        return minutes, seconds

    def current_score(self):
        return self.score

    def increase_score(self, score):
        self.score += score
        if self.score > self.best_score:
            self.best_score = self.score

    def highest_score(self):
        return self.best_score