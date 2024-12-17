import random

import pygame

from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.utils.astar_pathfinding import AStarPathfinding
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction
import src.utils.helper as helper
import src.utils.debugger as debugger


class Ghost(Sprite):
    # MODE
    FRIGHTENED = 1
    CHASE = 2
    SCATTER = 3
    DEAD = 4

    def __init__(self, animation, hitbox, ai_strategy):
        self.ai_strategy = ai_strategy
        self.mode = None
        self.is_frightened_flash = False
        self.last_time_switch_mode = 0
        self.mode_duration = 0
        super().__init__(animation, hitbox)

    def update(self):
        self._animation.update()
        if self.mode == Ghost.FRIGHTENED: self.update_frightened_animation()

    def execute_ai(self, maze):
        self.ai_strategy.execute(self, maze)

    def name(self): pass

    def switch_mode(self, mode, duration):
        self.mode = mode
        self.last_time_switch_mode = pygame.time.get_ticks()
        self.mode_duration = duration
        if mode == Ghost.FRIGHTENED:
            self._animation = Animation(self, 'frightened')
        elif mode == Ghost.DEAD:
            self._animation = Animation(self, 'ghost_dead')
        else: self._animation = Animation(self, self.name())

    def update_frightened_animation(self):
        duration = (pygame.time.get_ticks() - self.last_time_switch_mode) // 1000
        if duration > self.mode_duration - 2 and not self.is_frightened_flash:
            self._animation = Animation(self, 'frightened_flash')
            self.is_frightened_flash = True
        if duration > self.mode_duration:
            self.is_frightened_flash = False
            self.switch_mode(Ghost.CHASE, 10)

class GhostRed(Ghost):
    def __init__(self):
        animation = Animation(self, 'ghost_red')
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        super().__init__(animation, hitbox, RedAIStrategy())

    def name(self): return 'ghost_red'

class GhostOrange(Ghost):
    def __init__(self):
        animation = Animation(self, 'ghost_orange')
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        super().__init__(animation, hitbox, OrangeAIStrategy())

    def name(self): return 'ghost_orange'


### AI class

from abc import ABC, abstractmethod
class BasicAIStrategy(ABC):
    def __init__(self):
        self.scatter_step = 0
        self.algo = AStarPathfinding()

    @abstractmethod
    def execute(self,ghost, maze): pass

    def move_to(self, ghost, dest):
        path = self.algo.execute(ghost.get_position(), dest)
        if path is None :
            directs = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            ramdom_choice = random.choice(range(0,4))
            ghost.set_next_direction(directs[ramdom_choice])
        if path is not None and len(path) > 0:
            hitbox_center = ghost.get_hitbox().center

            c,r = ghost.get_position()

            # Tính trung tâm của ô hiện tại
            center_x = int(c * BLOCK_SIZE * SCALE + (BLOCK_SIZE * SCALE) // 2)
            center_y = int(r * BLOCK_SIZE * SCALE + (BLOCK_SIZE * SCALE) // 2)


            debugger.set_attributes('path', path)
            next = path[0].position
            dx = next[0] - ghost.get_position()[0]
            dy = next[1] - ghost.get_position()[1]
            if hitbox_center[0] == center_x and hitbox_center[1] == center_y:
                if dx > 0: ghost.set_next_direction(Direction.RIGHT)
                elif dx < 0: ghost.set_next_direction(Direction.LEFT)
                elif dy > 0: ghost.set_next_direction(Direction.DOWN)
                elif dy < 0: ghost.set_next_direction(Direction.UP)

class RedAIStrategy(BasicAIStrategy):
    SPAWN_ROW_COL = (14, 15)
    SPAWN_POS = (SPAWN_ROW_COL[1], SPAWN_ROW_COL[0])
    SCATTER_POS = [(1,1), (6,5)]
    SCATTER_DURATION = 10
    CHASE_DURATION = 20
    WAITING_DURATION = 3

    def execute(self, ghost, maze):
        self.auto_switch_mode(ghost)
        if ghost.mode == Ghost.CHASE:
            dest = maze.get_pacman_pos()
            ghost._speed = 2
        elif ghost.mode == Ghost.FRIGHTENED:
            dest = self.SPAWN_POS
            ghost._speed = 1
        elif ghost.mode == Ghost.SCATTER:
            ghost._speed = 2
            dest = self.SCATTER_POS[self.scatter_step]
            if ghost.get_position() == dest: self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        elif ghost.mode == Ghost.DEAD:
            ghost._speed = 5
            dest = self.SPAWN_POS
        else:
            dest = self.SPAWN_POS
            ghost._speed = 1

        self.move_to(ghost, dest)

    def auto_switch_mode(self, ghost):
        if ghost.mode == Ghost.FRIGHTENED: return
        if ghost.mode == Ghost.DEAD and ghost.get_position() == self.SPAWN_POS:
            ghost.mode_duration = 0
            ghost.mode = None
            return
        if ghost.last_time_switch_mode == 0: ghost.last_time_switch_mode = pygame.time.get_ticks()

        delta_time = (pygame.time.get_ticks() - ghost.last_time_switch_mode) // 1000

        if delta_time > self.WAITING_DURATION and ghost.mode is None:
            ghost.switch_mode(Ghost.SCATTER, self.SCATTER_DURATION)
        elif delta_time > self.SCATTER_DURATION and ghost.mode != Ghost.CHASE:
            ghost.switch_mode(Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.CHASE_DURATION and ghost.mode != Ghost.SCATTER:
            ghost.switch_mode(Ghost.SCATTER, self.SCATTER_DURATION)

class OrangeAIStrategy(BasicAIStrategy):
    SPAWN_ROW_COL = (14, 14)
    SPAWN_POS = (SPAWN_ROW_COL[1], SPAWN_ROW_COL[0])
    SCATTER_POS = [(1,1), (6,5)]
    SCATTER_DURATION = 10
    CHASE_DURATION = 20
    WAITING_DURATION = 4

    def execute(self, ghost, maze):
        self.auto_switch_mode(ghost)
        if ghost.mode == Ghost.CHASE:
            dest = maze.get_pacman_pos()
            ghost._speed = 2
        elif ghost.mode == Ghost.FRIGHTENED:
            dest = self.SPAWN_POS
            ghost._speed = 1
        elif ghost.mode == Ghost.SCATTER:
            ghost._speed = 2
            dest = self.SCATTER_POS[self.scatter_step]
            if ghost.get_position() == dest: self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        elif ghost.mode == Ghost.DEAD:
            ghost._speed = 5
            dest = self.SPAWN_POS
        else:
            dest = self.SPAWN_POS
            ghost._speed = 1

        self.move_to(ghost, dest)

    def auto_switch_mode(self, ghost):
        if ghost.mode == Ghost.FRIGHTENED: return
        if ghost.mode == Ghost.DEAD and ghost.get_position() == self.SPAWN_POS:
            ghost.mode_duration = 0
            ghost.mode = None
            return
        if ghost.last_time_switch_mode == 0: ghost.last_time_switch_mode = pygame.time.get_ticks()

        delta_time = (pygame.time.get_ticks() - ghost.last_time_switch_mode) // 1000

        if delta_time > self.WAITING_DURATION and ghost.mode is None:
            ghost.switch_mode(Ghost.SCATTER, self.SCATTER_DURATION)
        elif delta_time > self.SCATTER_DURATION and ghost.mode != Ghost.CHASE:
            ghost.switch_mode(Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.CHASE_DURATION and ghost.mode != Ghost.SCATTER:
            ghost.switch_mode(Ghost.SCATTER, self.SCATTER_DURATION)