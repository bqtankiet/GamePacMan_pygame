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
    EAT_GHOST = 2
    PACMAN_DIE = 3

    READY_TIME = 3000  # milliseconds
    DELAY_1S_TIME = 1000 # miliseconds

    def __init__(self, game):
        self.pacman = None
        self.__ghosts = []
        self.respawn()
        self.__grid = copy.deepcopy(MAZE_DATA)
        self.__collision_manager = CollisionManager(self.__grid)
        self.__start_time = pygame.time.get_ticks()
        self.__state = Maze.READY
        self.game = game
        self.maze_render = None

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.__state == Maze.PLAYING:
            self.update_entity(self.pacman)
            for g in self.__ghosts: self.update_entity(g)

        elif self.__state == Maze.READY:
            if self.__is_time_elapsed(current_time, Maze.READY_TIME):
                self.set_state(Maze.PLAYING)
            else: return

        elif self.__state == Maze.EAT_GHOST:
            if self.__is_time_elapsed(current_time, Maze.DELAY_1S_TIME):
                self.set_state(Maze.PLAYING)
            else: return

        elif self.__state == Maze.PACMAN_DIE:
            if self.__is_time_elapsed(current_time, Maze.DELAY_1S_TIME):
                if self.__ghosts: self.__ghosts = []
                self.pacman.update()
                if self.__is_time_elapsed(current_time, Maze.DELAY_1S_TIME*3.5):
                    if self.game.game_status.lives == 0:
                        game.Game.get_instance().switch_scene('GameOver')
                        return
                    self.respawn()
                    self.set_state(Maze.READY)
            else: return

    def respawn(self):
        self.add_entity(Pacman(), (23, 14))
        self.__ghosts = []
        self.add_entity(ghost.GhostRed(), ghost.RedAIStrategy.SPAWN_ROW_COL)
        # self.add_entity(ghost.GhostOrange(), ghost.OrangeAIStrategy.SPAWN_POS)
        # pass

    def update_entity(self, entity):
        entity.update()
        for _ in range(entity.get_speed()):
            self.handle_boundary_wrap(entity)
            self.handle_movement(entity)

            if isinstance(entity, Pacman):
                self.handle_pacman_collision(entity)
            elif isinstance(entity, ghost.Ghost):
                self.handle_ghost_ai(entity)

    def handle_boundary_wrap(self, entity):
        if entity.rect.right < 0:
            entity.rect.left = self.get_width()
        elif entity.rect.left > self.get_width():
            entity.rect.right = 0

    def handle_movement(self, entity):
        old_position = entity.rect.topleft
        if not self.__collision_manager.is_out_of_map(entity):
            if self.__collision_manager.can_move(entity, entity.get_next_direction()):
                entity.change_direction()

        entity.update_position()
        if self.__collision_manager.is_collide_wall(entity):
            entity.rect.topleft = old_position

    def handle_pacman_collision(self, pacman):
        for g in self.__ghosts:
            if pacman.collide(g):
                self.__handle_pacman_ghost_collision(pacman, g)

        r, c = helper.pixel_to_grid(pacman.get_hitbox().center)
        if not self.__collision_manager.is_out_of_map(pacman):
            self.__handle_pacman_pellet_collision(r, c)

    def __handle_pacman_ghost_collision(self, pacman, g):
        if g.mode == ghost.Ghost.DEAD: return
        if g.mode == ghost.Ghost.FRIGHTENED:
            self.set_state(Maze.EAT_GHOST)
            g.switch_mode(ghost.Ghost.DEAD, 99)
            self.game.game_status.increase_score(game.GameStatus.SCORE_GHOST)
            print("Pacman eat ghost")
        else:
            if self.__state == Maze.PACMAN_DIE: return
            self.set_state(Maze.PACMAN_DIE)
            self.pacman.die()
            self.game.game_status.decrease_lives()
            print("Pacman die")

    def __handle_pacman_pellet_collision(self, r, c):
        value = self.__grid[r][c]
        if value == self.PELLET:
            self.__grid[r][c] = 0
            self.game.game_status.increase_score(game.GameStatus.SCORE_PELLET)
        elif value == self.POWER_PELLET:
            self.__grid[r][c] = 0
            self.game.game_status.increase_score(game.GameStatus.SCORE_POWER_PELLET)
            for g in self.__ghosts:
                g.switch_mode(ghost.Ghost.FRIGHTENED, 5)
            print("Eat Power pellet")

    def handle_ghost_ai(self, entity):
        if not self.__collision_manager.is_out_of_map(self.pacman):
            entity.execute_ai(self)

    def add_entity(self, entity, row_col):
        if isinstance(entity, Pacman):
            debugger.set_attributes('hitbox', entity)
            self.pacman = entity
        elif isinstance(entity, ghost.Ghost):
            self.__ghosts.append(entity)

        x, y = helper.grid_to_pixel(row_col)
        x_center, y_center = x + helper.block_size_scaled / 2, y + helper.block_size_scaled / 2
        entity.get_hitbox().center = (x_center, y_center)
        entity.rect.center = (x_center, y_center)

    # getter, setter
    def get_pacman_pos(self):
        return self.pacman.get_position()

    def get_entities(self):
        return self.__ghosts + [self.pacman]

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
        self.__start_time = pygame.time.get_ticks()

    def set_maze_render(self, maze_render):
        self.maze_render = maze_render

    def __is_time_elapsed(self, current_time, duration):
        return (current_time - self.__start_time) >= duration


class CollisionManager:
    def __init__(self, grid):
        self.__grid = grid
        self.__block_size_scaled = BLOCK_SIZE * SCALE

    def can_move(self, entity, direction):
        old_xy = (entity.rect.x, entity.rect.y)
        self.__simulate_movement(entity, direction)
        result = not self.is_collide_wall(entity)
        entity.rect.x, entity.rect.y = old_xy
        return result

    def is_out_of_map(self, entity):
        width = len(self.__grid[0]) * self.__block_size_scaled
        height = len(self.__grid) * self.__block_size_scaled
        return not (0 < entity.rect.center[0] < width and 0 < entity.rect.center[1] < height)

    def is_collide_wall(self, entity):
        hitbox = entity.get_hitbox()
        corners = [
            hitbox.topleft,
            (hitbox.topright[0] - 1, hitbox.topright[1]),
            (hitbox.bottomleft[0], hitbox.bottomleft[1] - 1),
            (hitbox.bottomright[0] - 1, hitbox.bottomright[1] - 1)
        ]
        for corner in corners:
            r, c = helper.pixel_to_grid(corner)
            if 0 <= r < len(self.__grid) and 0 <= c < len(self.__grid[0]):
                if self.__grid[r][c] == Maze.WALL:
                    return True
        return False

    def __simulate_movement(self, entity, direction):
        if direction == Direction.LEFT:
            entity.rect.x -= Sprite.NORMAL_SPEED
        elif direction == Direction.RIGHT:
            entity.rect.x += Sprite.NORMAL_SPEED
        elif direction == Direction.UP:
            entity.rect.y -= Sprite.NORMAL_SPEED
        elif direction == Direction.DOWN:
            entity.rect.y += Sprite.NORMAL_SPEED


class MazeRender:
    def __init__(self, maze):
        self.__maze = maze
        self.__maze_image = ImageLoader().background_maze()
        self.__maze_surface = pygame.Surface(self.__maze_image.get_size())
        self.__area = self.__maze_image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.__maze = maze
        self.__maze.set_maze_render(self)

    def render(self):
        self.__maze_surface.fill("black")
        self.draw_maze()
        self.draw_entities()
        debugger.render(self.__maze_surface)

        if self.__maze.get_state() == Maze.READY:
            self.draw_ready_message()
        elif self.__maze.get_state() == Maze.EAT_GHOST:
            self.draw_score(game.GameStatus.SCORE_GHOST)

        return self.__maze_surface

    def draw_ready_message(self):
        message = ImageLoader().text_image("ready!", color="yellow")
        x = self.__maze.get_width() // 2
        y = self.__maze.get_height() // 2 + message.get_height() * 2
        self.__maze_surface.blit(message, message.get_rect(center=(x, y)))

    def draw_score(self, score):
        score_img = ImageLoader().score_100() if score == 100 else ImageLoader().score_200()
        x, y = self.__maze.get_pacman_pos()
        x = x * BLOCK_SIZE * SCALE + BLOCK_SIZE * SCALE // 2
        y = y * BLOCK_SIZE * SCALE - score_img.get_height() // 2
        self.__maze_surface.blit(score_img, score_img.get_rect(center=(x, y)))

    def draw_entities(self):
        # entities = pygame.sprite.Group(self.__maze.get_entities())
        # entities.draw(self.__maze_surface)
        for entity in self.__maze.get_entities():
            self.__maze_surface.blit(entity.image, entity.rect)

    def draw_maze(self):
        self.__maze_surface.blit(self.__maze_image, (0, 0))
        grid = self.__maze.get_grid()
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell == 0:
                    x = c * BLOCK_SIZE * SCALE
                    y = r * BLOCK_SIZE * SCALE
                    size = BLOCK_SIZE * SCALE
                    pygame.draw.rect(self.__maze_surface, "black", (x, y, size, size))
