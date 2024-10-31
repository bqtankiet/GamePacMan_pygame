import pygame

from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.utils.constant import SCALE, BLOCK_SIZE
from src.utils.enum import Direction


class Pacman(Sprite):
    def __init__(self):
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        animation = Animation(self, 'pacman')
        super().__init__(animation, hitbox)

    def update(self):
        """Cập nhật vị trí và animation của Pacman sau mỗi frame"""
        self.update_position()
        self._animation.update()