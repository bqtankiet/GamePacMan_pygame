import pygame

from src.entities.animation import Animation
from src.utils.constant import SCALE, BLOCK_SIZE
from src.utils.enum import Direction


class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = Direction.RIGHT
        self.next_direction = self.direction
        self.animation = Animation(self)
        self.image = self.animation.current()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, BLOCK_SIZE*SCALE, BLOCK_SIZE*SCALE)
        self.speed = 2

    def update(self, maze):
        self.update_position(maze)
        self.animation.update()

    def update_position(self, maze):
        old_x = self.rect.x
        old_y = self.rect.y
        if self.can_move(self.next_direction, maze): self.direction = self.next_direction
        if self.direction == Direction.LEFT: self.rect.x -= self.speed
        elif self.direction == Direction.RIGHT: self.rect.x += self.speed
        elif self.direction == Direction.UP: self.rect.y -= self.speed
        elif self.direction == Direction.DOWN: self.rect.y += self.speed
        self.hitbox.center = self.rect.center

        if self.collide_wall(maze):
            self.rect.x = old_x
            self.rect.y = old_y
            self.hitbox.center = self.rect.center

    def can_move(self, direction, maze):
        result = True
        old_x = self.rect.x
        old_y = self.rect.y
        if direction == Direction.LEFT: self.rect.x -= self.speed
        elif direction == Direction.RIGHT: self.rect.x += self.speed
        elif direction == Direction.UP: self.rect.y -= self.speed
        elif direction == Direction.DOWN: self.rect.y += self.speed
        self.hitbox.center = self.rect.center

        if self.collide_wall(maze):
            result = False
        self.rect.x = old_x
        self.rect.y = old_y
        self.hitbox.center = self.rect.center
        return result

    def get_hitbox(self):
        return self.hitbox

    def collide(self, sprite):
        return self.get_hitbox().colliderect(sprite.get_hitbox())

    def collide_wall(self, maze):
        hitbox = self.hitbox
        topleft = (hitbox.topleft[0], hitbox.topleft[1])
        topright = (hitbox.topright[0]-1, hitbox.topright[1])
        bottomleft = (hitbox.bottomleft[0], hitbox.bottomleft[1]-1)
        bottomright = (hitbox.bottomright[0]-1, hitbox.bottomright[1]-1)
        for i in (topleft, topright, bottomleft, bottomright):
            r = int(i[1]/(BLOCK_SIZE*SCALE))
            c = int(i[0]/(BLOCK_SIZE*SCALE))
            if maze.grid[r][c] == 1: return True
        return False