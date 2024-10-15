import pygame

from src.entities.animation import Animation
from src.utils.constant import SCALE, BLOCK_SIZE
from src.utils.enum import Direction


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = Direction.DOWN
        self.next_direction = self.direction
        self.animation = Animation(self)
        self.image = self.animation.current()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, BLOCK_SIZE*SCALE-2, BLOCK_SIZE*SCALE-2)
        self.speed = 2

    def update(self):
        """Cập nhật vị trí và animation của Pacman sau mỗi frame"""
        self.update_position()
        self.animation.update()

    def update_position(self):
        match self.direction:
            case Direction.RIGHT: self.rect.x += self.speed
            case Direction.LEFT: self.rect.x -= self.speed
            case Direction.UP: self.rect.y -= self.speed
            case Direction.DOWN: self.rect.y += self.speed

    def get_hitbox(self):
        self.hitbox.center = self.rect.center
        return self.hitbox

    def collide(self, sprite):
        """Phương thức kiểm tra va chạm giữa 2 sprite
        Return True nếu va chạm xảy ra. Ngược lại return về False"""
        return self.get_hitbox().colliderect(sprite.get_hitbox())

