import random

import pygame
from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.utils.astar_pathfinding import AStarPathfinding
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction
import src.utils.debugger as debugger


class Ghost(Sprite):
    # MODE
    FRIGHTENED = 1
    CHASE = 2
    SCATTER = 3
    DEAD = 4

    def __init__(self, animation, hitbox):
        self.algo = AStarPathfinding()
        self.mode = None
        self.last_frightened = 0
        self.frightened_duration = 5
        self.is_frightened_flash = False
        self.last_time_switch_mode = 0
        super().__init__(animation, hitbox)

    def update(self):
        # self.update_position()
        self._animation.update()
        if self.mode == Ghost.FRIGHTENED: self.update_frightened()

    def update_frightened(self):
        duration = (pygame.time.get_ticks() - self.last_frightened) // 1000
        if duration > self.frightened_duration - 2 and not self.is_frightened_flash:
            self._animation = Animation(self, 'frightened_flash')
            self.is_frightened_flash = True
        if duration > self.frightened_duration:
            self.is_frightened_flash = False
            self.chase()

    def execute_ai(self, maze):
        pass

    def name(self):
        pass

    def frightened(self):
        self.mode = Ghost.FRIGHTENED
        self.last_frightened = pygame.time.get_ticks()
        self._animation = Animation(self, 'frightened')

    def scatter(self):
        self.mode = Ghost.SCATTER
        self._animation = Animation(self, self.name())

    def chase(self):
        self.mode = Ghost.CHASE
        self._animation = Animation(self, self.name())

    def is_frightened(self):
        return self.mode == Ghost.FRIGHTENED

    def move_to(self, dest):
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


class GhostRed(Ghost):
    SCATTER_POS = [(1,1), (6,1), (6,5)]
    SCATTER_DURATION = 10
    CHASE_DURATION = 20
    WAITING_DURATION = 3

    def __init__(self):
        animation = Animation(self, 'ghost_red')
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        self.scatter_step = 0
        super().__init__(animation, hitbox)

    def execute_ai(self, maze):
        self.auto_switch_mode()
        if self.mode == Ghost.CHASE:
            dest = maze.get_pacman_pos()
            self._speed = 2
        elif self.mode == Ghost.FRIGHTENED:
            dest = (14, 14)
            self._speed = 1
        elif self.mode == Ghost.SCATTER:
            self._speed = 2
            dest = GhostRed.SCATTER_POS[self.scatter_step]
            if self.get_position() == dest: self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        else:
            dest = (14, 14)
            self._speed = 1

        self.move_to(dest)

    def auto_switch_mode(self):
        if self.mode == self.FRIGHTENED: return
        if self.last_time_switch_mode == 0: self.last_time_switch_mode = pygame.time.get_ticks()
        if (pygame.time.get_ticks() - self.last_time_switch_mode) // 1000 > self.WAITING_DURATION and self.mode is None:
            self.last_time_switch_mode = pygame.time.get_ticks()
            self.scatter()
        elif (pygame.time.get_ticks() - self.last_time_switch_mode) // 1000 > self.SCATTER_DURATION and self.mode != Ghost.CHASE:
            self.last_time_switch_mode = pygame.time.get_ticks()
            self.chase()
        elif (pygame.time.get_ticks() - self.last_time_switch_mode) // 1000 > self.CHASE_DURATION and self.mode != Ghost.SCATTER:
            self.last_time_switch_mode = pygame.time.get_ticks()
            self.scatter()

    def name(self): return 'ghost_red'