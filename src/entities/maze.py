import pygame

import src.utils.debugger as debugger
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader


class Maze:
    WALL = 1

    def __init__(self):
        self.image = ImageLoader().background_maze()
        self.grid = self.get_grid()
        self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.pacman = None
        self.block_size_scaled = BLOCK_SIZE * SCALE
        # debugger.draw_grid(self.image)

    def render(self):
        """Vẽ hình ảnh của các entity và mê cung lên surface"""
        self.surface.fill("black")
        self.surface.blit(self.image, (0, 0))
        self.draw_entity(self.pacman)
        # debugger.draw_hitbox(self.surface, self.pacman)

    def draw_entity(self, pacman):
        """Vẽ entity lên surface
        Nhận vào một entity và vẽ nó lên surface của mê cung"""
        self.surface.blit(self.pacman.image, self.pacman.rect)

    def update(self):
        """Cập nhật trạng thái của mê cung sau mỗi frame"""
        #update Pacman
        self.update_pacman()
        #update Ghosts
        #update Maze
        #render surface
        self.render()

    def update_pacman(self):
        """Xử lý các logic cập nhật cho Pacman"""
        old_position = self.pacman.rect.topleft
        """Pacman tele khi đi vào đường tắt ( DONE )"""
        if self.can_move(self.pacman, self.pacman.next_direction):
            self.pacman.direction = self.pacman.next_direction

        # Cập nhật vị trí Pacman dựa trên hướng hiện tại
        self.pacman.update()

        # Kiểm tra va chạm tường, nếu có thì hoàn nguyên vị trí
        if self.collide_wall(self.pacman):
            self.pacman.rect.topleft = old_position

        # Xử lý nếu Pacman ra ngoài biên trái hoặc phải của map
        if self.pacman.rect.left < 0:
            self.pacman.rect.right = len(self.grid[0]) * self.block_size_scaled
        elif self.pacman.rect.right > len(self.grid[0]) * self.block_size_scaled:
            self.pacman.rect.left = 0

        # Kiểm tra lại hướng sau khi vượt biên map
        if self.can_move(self.pacman, self.pacman.direction):
            self.pacman.update()

    def add_pacman(self, pacman, position):
        """Thêm Pacman vào Mê cung"""
        self.pacman = pacman
        x, y = self.grid_to_pixel(position)
        pacman.hitbox.center = (x, y)
        pacman.rect.center = (x, y)

    def collide_wall(self, entity):
        """Kiểm tra va chạm giữa thực thể và tường trong mê cung"""
        hitbox = entity.get_hitbox()
        topleft = hitbox.topleft
        topright = (hitbox.topright[0] - 1, hitbox.topright[1])
        bottomleft = (hitbox.bottomleft[0], hitbox.bottomleft[1] - 1)
        bottomright = (hitbox.bottomright[0] - 1, hitbox.bottomright[1] - 1)

        for corner in (topleft, topright, bottomleft, bottomright):
            r, c = self.pixel_to_grid(corner)
            if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[0]):  # Kiểm tra chỉ số
                continue  # Bỏ qua nếu chỉ số không hợp lệ
            if self.grid[r][c] == Maze.WALL:
                return True
        return False

    def can_move(self, entity, direction):
        """Kiểm tra xem thực thể có thê di chuyển theo hướng cho trước hay không"""
        result = True
        old_xy = (entity.rect.x, entity.rect.y)
        if direction == Direction.LEFT: entity.rect.x -= entity.speed
        elif direction == Direction.RIGHT: entity.rect.x += entity.speed
        elif direction == Direction.UP: entity.rect.y -= entity.speed
        elif direction == Direction.DOWN: entity.rect.y += entity.speed

        if self.collide_wall(entity): result = False

        entity.rect.x = old_xy[0]
        entity.rect.y = old_xy[1]
        return result

    def grid_to_pixel(self, position):
        """Chuyển đổi vị trí ô trong lưới sang vị trí pixel"""
        x = (position[1] * self.block_size_scaled) + (self.block_size_scaled / 2)
        y = (position[0] * self.block_size_scaled) + (self.block_size_scaled / 2)
        return x, y

    def pixel_to_grid(self, position):
        """Chuyển đổi một vị trí pixel thành vị trí ô trong lưới"""
        x, y = position
        r = int(y / self.block_size_scaled)
        c = int(x / self.block_size_scaled)

        # Kiểm tra chỉ số trước khi trả về
        if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[0]):
            return -1, -1  # Trả về chỉ số không hợp lệ
        return r, c

    def get_image(self):
        return self.image

    def get_grid(self):
        return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]