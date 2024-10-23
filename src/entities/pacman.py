import pygame

from src.entities.animation import Animation
from src.utils.constant import SCALE, BLOCK_SIZE
from src.utils.enum import Direction


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__direction = Direction.DOWN
        self.__next_direction = self.__direction
        self.__hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        self.__speed = 2
        self.__animation = Animation(self)

        # 2 thuộc tính này kế thừa từ lớp pygame.Sprite (lây thông tin để vẽ sprite)
        self.image = self.__animation.current()
        self.rect = self.image.get_rect()


    def update(self):
        """Cập nhật vị trí và animation của Pacman sau mỗi frame"""
        self.update_position()
        self.__animation.update()

    def update_position(self):
        match self.__direction:
            case Direction.RIGHT:
                self.rect.x += self.__speed
            case Direction.LEFT:
                self.rect.x -= self.__speed
            case Direction.UP:
                self.rect.y -= self.__speed
            case Direction.DOWN:
                self.rect.y += self.__speed

    def get_hitbox(self):
        self.__hitbox.center = self.rect.center
        return self.__hitbox

    def collide(self, sprite):
        """Phương thức kiểm tra va chạm giữa 2 sprite
        Return True nếu va chạm xảy ra. Ngược lại return về False"""
        return self.get_hitbox().colliderect(sprite.get_hitbox())

    #----------------------------------------
    # Getter, Setter
    #----------------------------------------
    def get_direction(self):
        return self.__direction

    def get_next_direction(self):
        return self.__next_direction

    def get_speed(self):
        return self.__speed

    def set_next_direction(self, direction: Direction):
        self.__next_direction = direction

    def change_direction(self):
        if self.__next_direction:
            self.__direction = self.__next_direction