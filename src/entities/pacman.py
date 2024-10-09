import pygame

from src.entities.animation import Animation
from src.utils.enum import Direction


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = Direction.RIGHT
        self.animation = Animation(self)
        self.image = self.animation.current()
        self.rect = self.image.get_rect()
        self.speed = 2

    def update(self):
        self.update_position()
        self.animation.update()

    def update_position(self):
        if self.direction == Direction.LEFT: self.rect.x -= self.speed
        elif self.direction == Direction.RIGHT: self.rect.x += self.speed
        elif self.direction == Direction.UP: self.rect.y -= self.speed
        elif self.direction == Direction.DOWN: self.rect.y += self.speed
