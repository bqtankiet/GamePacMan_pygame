import sys

import pygame

import src.utils.constant as const
from src.scenes.game_over import GameOver
from src.scenes.gameplay import GamePlay
from src.scenes.main_menu import MainMenu
from src.scenes.pause_game import PauseGame


class Game:
    def __init__(self):
        # init pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('PacMan')

        # init attributes
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT), pygame.FULLSCREEN)
        self.scenes = {
            "MainMenu": MainMenu(self),
            "GamePlay": GamePlay(self),
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

