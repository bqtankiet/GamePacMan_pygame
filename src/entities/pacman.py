import pygame

from src.entities.animation import Animation


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = "right"
        self.animation = Animation(self)
        self.image = self.animation.current()
        self.rect = self.image.get_rect()
        self.speed = 2

    def update(self):
        self.update_position()
        self.animation.update()

    def update_position(self):
        if self.direction == "left": self.rect.x -= self.speed
        elif self.direction == "right": self.rect.x += self.speed
        elif self.direction == "up": self.rect.y -= self.speed
        elif self.direction == "down": self.rect.y += self.speed
