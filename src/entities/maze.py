import copy

import pygame

import src.entities.ghost as ghost
from src.entities.pacman import Pacman
from src.utils.constant import BLOCK_SIZE, SCALE, WIDTH, HEIGHT, MAZE_DATA
from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader
import src.utils.helper as helper
import src.utils.debugger as debugger


class Maze:
    WALL = 1
    PELLET = 2
    POWER_PELLET = 3

    def __init__(self):
        self.__grid = copy.deepcopy(MAZE_DATA)
        # self.__entities = []
        self.__collision_manager = CollisionManager(self.__grid)
        self.__pacman = None
        self.__ghosts = []

    def update(self):
        # update pacman
        self.update_entity(self.__pacman)
        # update ghosts
        for g in self.__ghosts: self.update_entity(g)

    def update_entity(self, entity):
        # Xử lý khi pacman/ghost đi ra khỏi rìa map -> dịch chuyển
        if entity.rect.right < 0:
            entity.rect.left = self.get_width()
        elif entity.rect.left > self.get_width():
            entity.rect.right = 0

        # cập nhật hướng di chuyển của pacman/ghost
        old_position = entity.rect.topleft
        if not self.__collision_manager.is_out_of_map(entity):
            if self.__collision_manager.can_move(entity, entity.get_next_direction()):
                    entity.change_direction()
        
        # Cập nhật vị trí của pacman/ghost
        entity.update()
        if self.__collision_manager.is_collide_wall(entity):
            entity.rect.topleft = old_position

        # Xử lý pacman ăn pellet
        if isinstance(entity, Pacman):
            pacman = entity
            for g in self.__ghosts:
                if pacman.collide(g):
                    # TODO: Xử lý khi pacman va chạm ghost
                    print("Pacman collide ghost")

            r, c = helper.pixel_to_grid(pacman.get_hitbox().center)
            if not self.__collision_manager.is_out_of_map(pacman):
                value = self.__grid[r][c]
                if value == self.PELLET:
                    self.__grid[r][c] = 0
                if value == self.POWER_PELLET:
                    self.__grid[r][c] = 0
                    # TODO: Xử lý khi ăn hạt năng lượng lớn
                    print("Eat Power pellet")

        print(self.__pacman.get_position())
        # Xử lý ghost
        if isinstance(entity, ghost.Ghost):
            # entity.execute_ai(self.__pacman.get_position())
            if not self.__collision_manager.is_out_of_map(self.__pacman):
                entity.execute_ai(self.__pacman.get_position())

    def add_entity(self, entity, position):
        if isinstance(entity, Pacman):
            debugger.set_attributes('hitbox', entity)
            self.__pacman = entity
        elif isinstance(entity, ghost.Ghost): self.__ghosts.append(entity)
        x, y = helper.grid_to_pixel(position)
        entity.get_hitbox().center = (x, y)
        entity.rect.center = (x, y)

    def get_entities(self):
        entities = [g for g in self.__ghosts]
        entities.append(self.__pacman)
        return entities

    def get_grid(self):
        return self.__grid

    def get_width(self):
        return len(self.__grid[0]) * BLOCK_SIZE * SCALE

    def get_height(self):
        return len(self.__grid) * BLOCK_SIZE * SCALE

class CollisionManager:
    """Class phụ trách việc kiểm tra và xử lý chạm"""
    def __init__(self, grid):
        self.__grid = grid
        self.__block_size_scaled = BLOCK_SIZE * SCALE

    def can_move(self, entity, direction):
        """Kiểm tra xem thực thể có thê di chuyển theo hướng cho trước hay không"""
        result = True
        old_xy = (entity.rect.x, entity.rect.y)
        if direction == Direction.LEFT:
            entity.rect.x -= entity.get_speed()
        elif direction == Direction.RIGHT:
            entity.rect.x += entity.get_speed()
        elif direction == Direction.UP:
            entity.rect.y -= entity.get_speed()
        elif direction == Direction.DOWN:
            entity.rect.y += entity.get_speed()

        if self.is_collide_wall(entity): result = False

        entity.rect.x = old_xy[0]
        entity.rect.y = old_xy[1]
        return result

    def is_out_of_map(self, entity):
        width = len(self.__grid[0]) * self.__block_size_scaled
        height = len(self.__grid) * self.__block_size_scaled
        return not 0 < entity.rect.center[0] < width and 0 < entity.rect.center[1] < height

    def is_collide_wall(self, entity):
        """Kiểm tra va chạm giữa thực thể và tường"""
        hitbox = entity.get_hitbox()
        corners = [
            hitbox.topleft,
            (hitbox.topright[0] - 1, hitbox.topright[1]),
            (hitbox.bottomleft[0], hitbox.bottomleft[1] - 1),
            (hitbox.bottomright[0] - 1, hitbox.bottomright[1] - 1)
        ]
        for corner in corners:
            r, c = helper.pixel_to_grid(corner)
            if r < 0 or c < 0 or r >= len(self.__grid) or c >= len(self.__grid[0]): continue
            if self.__grid[r][c] == Maze.WALL:
                return True
        return False

class MazeRender:
    def __init__(self, maze):
        self.__maze_image = self.__image = ImageLoader().background_maze()
        self.__maze_surface = pygame.Surface((self.__maze_image.get_size()))
        self.__entities = pygame.sprite.Group(maze.get_entities())
        self.__area = self.__image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.__maze = maze

    def render(self):
        self.draw_maze()
        self.draw_entities()
        debugger.render(self.__maze_surface)
        return self.__maze_surface

    def draw_entities(self):
        self.__entities.draw(self.__maze_surface)

    def draw_maze(self):
        self.__maze_surface.fill("black")
        self.__maze_surface.blit(self.__maze_image, (0, 0))
        grid = self.__maze.get_grid()
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 0:
                    x = c * BLOCK_SIZE * SCALE
                    y = r * BLOCK_SIZE * SCALE
                    size = BLOCK_SIZE * SCALE
                    pygame.draw.rect(self.__maze_surface, "black", (x, y, size, size))