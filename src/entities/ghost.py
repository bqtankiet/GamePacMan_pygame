import random

import pygame
from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.utils.astar_pathfinding import AStarPathfinding
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction


class Ghost(Sprite):
    def __init__(self, animation, hitbox):
        self.algo = AStarPathfinding()
        super().__init__(animation, hitbox)

    def update(self):
        self.update_position()
        self._animation.update()

    def execute_ai(self, dest):
        pass

class GhostRed(Ghost):
    def __init__(self):
        animation = Animation(self, 'ghost_red')
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        super().__init__(animation, hitbox)

    def execute_ai(self, dest):
        path = self.algo.execute(self.get_position(), dest)
        if path is None :
            directs = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            ramdom_choice = random.choice(range(0,4))
            self.set_next_direction(directs[ramdom_choice])
        if path is not None and len(path) > 0:
            next = path[0].position
            dx = next[0] - self.get_position()[0]
            dy = next[1] - self.get_position()[1]
            print(self.get_position(), next)
            print(dx, dy)
            if dx > 0: self.set_next_direction(Direction.RIGHT)
            elif dx < 0: self.set_next_direction(Direction.LEFT)
            elif dy > 0: self.set_next_direction(Direction.DOWN)
            elif dy < 0: self.set_next_direction(Direction.UP)
            print(self._next_direction)