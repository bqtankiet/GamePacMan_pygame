import pygame
from abc import ABC, abstractmethod

from utils.constant import HEIGHT, WIDTH

class Scene(ABC):
    def __init__(self) -> None:
        self._surface = pygame.Surface((WIDTH, HEIGHT))
        self._surface.fill("BLACK")
        self.renderSurface()
    
    def draw(self, surface):
        surface.blit(self._surface, (0, 0))

    @abstractmethod
    def renderSurface(self): pass

    @abstractmethod
    def handle_event(self, event): pass

    @abstractmethod
    def update(self): pass
