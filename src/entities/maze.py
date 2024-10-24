import pygame

from src.utils.constant import BLOCK_SIZE, SCALE, WIDTH, HEIGHT, MAZE_DATA
from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader


class Maze:
    WALL = 1

    def __init__(self):
        self.__grid = self.get_grid()
        self.__entities = []
        self.__collision_manager = CollisionManager(self.__grid)

    def update(self):
        for entity in self.__entities:
            self.update_entity(entity)

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


    def get_width(self):
        return len(self.__grid[0]) * BLOCK_SIZE * SCALE

    def get_height(self):
        return len(self.__grid) * BLOCK_SIZE * SCALE

    def add_pacman(self, pacman, position):
        """Thêm Pacman vào Mê cung"""
        self.__entities.append(pacman)
        x, y = self.__collision_manager.grid_to_pixel(position)
        pacman.get_hitbox().center = (x, y)
        pacman.rect.center = (x, y)

    def get_entities(self):
        return self.__entities

    def get_grid(self):
        return MAZE_DATA

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
            r, c = self.pixel_to_grid(corner)
            if r < 0 or c < 0 or r >= len(self.__grid) or c >= len(self.__grid[0]): continue
            if self.__grid[r][c] == Maze.WALL:
                return True
        return False

    def pixel_to_grid(self, position):
        """Chuyển đổi pixel thành vị trí trong lưới"""
        x, y = position
        r = int(y / self.__block_size_scaled)
        c = int(x / self.__block_size_scaled)
        return r, c

    def grid_to_pixel(self, position):
        """Chuyển đổi vị trí ô trong lưới sang vị trí pixel"""
        x = (position[1] * self.__block_size_scaled) + (self.__block_size_scaled / 2)
        y = (position[0] * self.__block_size_scaled) + (self.__block_size_scaled / 2)
        return x, y

class MazeRender:
    def __init__(self, maze):
        self.__maze_image = self.__image = ImageLoader().background_maze()
        self.__maze_surface = pygame.Surface((self.__maze_image.get_size()))
        self.__entities = pygame.sprite.Group(maze.get_entities())
        self.__area = self.__image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    def render(self):
        self.draw_maze()
        self.draw_entities()
        return self.__maze_surface

    def draw_entities(self):
        self.__entities.draw(self.__maze_surface)

    def draw_maze(self):
        self.__maze_surface.fill("black")
        self.__maze_surface.blit(self.__maze_image, (0, 0))