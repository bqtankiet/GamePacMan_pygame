import random

import pygame
from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.utils.astar_pathfinding import AStarPathfinding
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction
import src.utils.debugger as debugger


class Ghost(Sprite):
    def __init__(self, animation, hitbox):
        self.algo = AStarPathfinding()
        self.is_frightened = False
        self.last_frightened = 0
        self.frightened_duration = 5
        self.is_frightened_flash = False
        super().__init__(animation, hitbox)

    def update(self):
        self.update_position()
        self._animation.update()
        if self.is_frightened:
            duration = (pygame.time.get_ticks() - self.last_frightened)//1000
            if duration > self.frightened_duration-2 and not self.is_frightened_flash:
                self._animation = Animation(self, 'frightened_flash')
                self.is_frightened_flash = True
            if duration > self.frightened_duration:
                self.is_frightened_flash = False
                self.is_frightened = False
                self._animation = Animation(self, self.name())

    def execute_ai(self, dest):
        pass

    def name(self):
        pass

    def frightened(self):
        self.is_frightened = True
        self.last_frightened = pygame.time.get_ticks()
        self._animation = Animation(self, 'frightened')

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
            debugger.set_attributes('path', path)
            next = path[0].position
            dx = next[0] - self.get_position()[0]
            dy = next[1] - self.get_position()[1]
            if dx > 0: self.set_next_direction(Direction.RIGHT)
            elif dx < 0: self.set_next_direction(Direction.LEFT)
            elif dy > 0: self.set_next_direction(Direction.DOWN)
            elif dy < 0: self.set_next_direction(Direction.UP)

    def name(self): return 'ghost_red'