import sys

import pygame

from src.scenes.gameplay import GamePlay
from src.scenes.main_menu import MainMenu
from src.utils.constant import HEIGHT, WIDTH


class Game:
    def __init__(self):
            # init pygame
            pygame.init()
            pygame.mouse.set_visible(False)
            pygame.display.set_caption('PacMan')

            # init attributes
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.scenes = {
                 "MainMenu": MainMenu(self),
                 "GamePlay": GamePlay(self)
            }
            self.current_scene = self.scenes["MainMenu"]
            self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False

            self.current_scene.handle_event()
            self.current_scene.update()
            self.current_scene.render()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def switch_scene(self, scene_name):
        self.current_scene = self.scenes[scene_name]