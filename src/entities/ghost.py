import random

import pygame
from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.entities.maze import CollisionManager
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction


class Ghost(Sprite):
    def __init__(self):
        animation = Animation(self, 'ghost_red')
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        super().__init__(animation, hitbox)

    def update(self):
        self.update_position()
        self._animation.update()

    def execute_ai(self, collision_manage :CollisionManager):
        if not collision_manage.can_move(self, self.get_direction()):
            directs = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            ramdom_choice = random.choice(range(0,4))
            self.set_next_direction(directs[ramdom_choice])
