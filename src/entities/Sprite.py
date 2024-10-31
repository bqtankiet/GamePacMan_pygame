import pygame.sprite
from pygame.examples.cursors import image

from src.entities.animation import Animation
from src.utils.enum import Direction


class Sprite(pygame.sprite.Sprite):
    def __init__(self, animation: Animation, hitbox):
        super().__init__()
        self._animation = animation
        self._hitbox = hitbox
        self._speed = 2
        self._direction = Direction.DOWN
        self._next_direction = self._direction
        
        self.image = animation.current()
        self.rect = self.image.get_rect()

    def update_position(self):
        match self._direction:
            case Direction.RIGHT:
                self.rect.x += self._speed
            case Direction.LEFT:
                self.rect.x -= self._speed
            case Direction.UP:
                self.rect.y -= self._speed
            case Direction.DOWN:
                self.rect.y += self._speed

    def get_hitbox(self):
        self._hitbox.center = self.rect.center
        return self._hitbox

    def collide(self, sprite):
        """Phương thức kiểm tra va chạm giữa 2 sprite
        Return True nếu va chạm xảy ra. Ngược lại return về False"""
        return self.get_hitbox().colliderect(sprite.get_hitbox())
    #----------------------------------------
    # Getter, Setter
    #----------------------------------------
    def get_direction(self):
        return self._direction

    def get_next_direction(self):
        return self._next_direction

    def get_speed(self):
        return self._speed

    def set_next_direction(self, direction: Direction):
        self._next_direction = direction

    def change_direction(self):
        if self._next_direction:
            self._direction = self._next_direction