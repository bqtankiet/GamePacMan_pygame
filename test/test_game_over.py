import sys

import pygame

import src.utils.constant as const
from src.scenes.game_over import GameOver
from src.scenes.pause_game import PauseGame


class TestPauseGame:
    def __init__(self):
        # init pygame
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('PacMan')

        # init attributes
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT), pygame.FULLSCREEN)
        self.current_scene = GameOver(self)
        self.running = True

    def run(self):
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

if __name__ == '__main__':
    TestPauseGame().run()