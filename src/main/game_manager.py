import sys
from turtle import Screen
import pygame

from scene.main_menu import MainMenu
from utils.constant import HEIGHT, WIDTH

class GameManager:
    """Singleton"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.initialized = True
            pygame.init()
            pygame.mouse.set_visible(False)
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()
            self.current_scene = MainMenu()

    def run(self):
        self.running = True
        while(self.running):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT): running = False
                else: self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.draw(self.screen)

            self.clock.tick(60)

            pygame.display.update()
        pygame.quit()
        sys.exit()