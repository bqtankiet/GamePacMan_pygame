import copy

import pygame

import src.entities.ghost as ghost
import src.core.game as game
from src.entities.Sprite import Sprite
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
    READY = 0
    PLAYING = 1

    def __init__(self, game):
        self.__grid = copy.deepcopy(MAZE_DATA)
        # self.__entities = []
        self.__collision_manager = CollisionManager(self.__grid)
        self.__pacman = None
        self.__ghosts = []
        self.__start_time = pygame.time.get_ticks()
        self.__state = Maze.READY
        self.game = game

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.__state == Maze.READY:
            if current_time - self.__start_time > 3000:
                self.__state = Maze.PLAYING
            return

        # update pacman
        self.update_entity(self.__pacman)
        # update ghosts
        for g in self.__ghosts: self.update_entity(g)

    def update_entity(self, entity):
        entity.update()
        for i in range(entity.get_speed()):
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

            entity.update_position()
            # Cập nhật vị trí của pacman/ghost
            if self.__collision_manager.is_collide_wall(entity):
                print(entity.rect.topleft, old_position)
                entity.rect.topleft = old_position

        # Xử lý pacman ăn pellet
        if isinstance(entity, Pacman):
            pacman = entity
            for g in self.__ghosts:
                if pacman.collide(g):
                    # TODO: Xử lý khi pacman va chạm ghost
                    print("Pacman collide ghost")
                    if g.mode == ghost.Ghost.FRIGHTENED:
                        g.switch_mode(ghost.Ghost.DEAD, 99)
                        self.game.game_status.increase_score(game.GameStatus.SCORE_PELLET)
                        print("Pacman eat ghost")
                    else: print("Pacman die")

            r, c = helper.pixel_to_grid(pacman.get_hitbox().center)
            if not self.__collision_manager.is_out_of_map(pacman):
                value = self.__grid[r][c]
                if value == self.PELLET:
                    # TODO: Xử lý khi ăn hạt thường
                    self.__grid[r][c] = 0
                    self.game.game_status.increase_score(game.GameStatus.SCORE_PELLET)
                if value == self.POWER_PELLET:
                    self.__grid[r][c] = 0
                    # TODO: Xử lý khi ăn hạt năng lượng lớn
                    self.game.game_status.increase_score(game.GameStatus.SCORE_POWER_PELLET)
                    for g in self.__ghosts: g.switch_mode(ghost.Ghost.FRIGHTENED, 5)
                    print("Eat Power pellet")

        print(self.__pacman.get_position())
        # Xử lý ghost
        if isinstance(entity, ghost.Ghost):
            if not self.__collision_manager.is_out_of_map(self.__pacman):
                entity.execute_ai(self)

    def add_entity(self, entity, position):
        if isinstance(entity, Pacman):
            debugger.set_attributes('hitbox', entity)
            self.__pacman = entity
        elif isinstance(entity, ghost.Ghost): self.__ghosts.append(entity)
        x, y = helper.grid_to_pixel(position)
        x_center, y_center = x+helper.block_size_scaled/2, y+helper.block_size_scaled/2
        entity.get_hitbox().center = (x_center, y_center)
        entity.rect.center = (x_center, y_center)

    def get_pacman_pos(self):
        return self.__pacman.get_position()

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

    def get_state(self):
        return self.__state

    def set_state(self, state):
        self.__state = state
        if state == Maze.READY:
            self.__start_time = pygame.time.get_ticks()

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
            entity.rect.x -= Sprite.NORMAL_SPEED
        elif direction == Direction.RIGHT:
            entity.rect.x += Sprite.NORMAL_SPEED
        elif direction == Direction.UP:
            entity.rect.y -= Sprite.NORMAL_SPEED
        elif direction == Direction.DOWN:
            entity.rect.y += Sprite.NORMAL_SPEED

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

        if self.__maze.get_state() == Maze.READY:
            self.draw_ready_message()

        return self.__maze_surface

    def draw_ready_message(self):
        message = ImageLoader().text_image("ready!")
        x = self.__maze.get_width()//2
        y = self.__maze.get_height()//2 + message.get_height()*2
        self.__maze_surface.blit(message, message.get_rect(center=(x, y)))

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