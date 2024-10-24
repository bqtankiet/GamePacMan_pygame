from abc import ABC, abstractmethod

import pygame

from src.utils.constant import HEIGHT, WIDTH


class Scene(ABC):
    """Abstract class dùng để tạo ra các màn hình của Game"""

    def __init__(self, game):
        self._game = game
        self._surface = pygame.Surface((WIDTH, HEIGHT))
        self._surface.fill("BLACK")

    def render(self):
        """Phương thức dùng để hiện thị màn hình hiện tại lên mành hình chính"""
        self._game.screen.blit(self._surface, (0, 0))

    @abstractmethod
    def render_surface(self):
        """Các class con cần override phương thức này để vẽ các hình ảnh lên surface của nó"""
        pass

    @abstractmethod
    def handle_event(self, event):
        """Các class con cần override phương thức này để xử lý các sự kiện"""
        pass

    @abstractmethod
    def update(self):
        """Các class con cần override phương thức này để cập nhật màn hình sau mỗi frame"""
        pass

    @abstractmethod
    def reset(self):
        """Phương thức này dùng để reset màn hình về trạng thái ban đầu"""
        pass
