import sys
import pygame

from scene.gameplay import GamePlay
from scene.main_menu import MainMenu
from utils.constant import HEIGHT, WIDTH

class GameManager:
    def __init__(self):
            pygame.init()
            pygame.mouse.set_visible(False)
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()
            self.scenes = {
                 MainMenu.__name__: MainMenu(self),
                 GamePlay.__name__: GamePlay(self)
            }
            self.current_scene = self.scenes[MainMenu.__name__]

    def run(self):
        self.running = True
        while(self.running):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT): running = False
                else: self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def switch_scene(self, scene_name):
        self.current_scene = self.scenes[scene_name]