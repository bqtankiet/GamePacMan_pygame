import pygame.draw

from src.utils.constant import BLOCK_SIZE, SCALE

"""Module phục vụ cho việc debug"""


def draw_hitbox(surface, sprite):
    """Nhận vào một surface, sprite và vẽ hitbox của sprite đó lên surface"""
    pygame.draw.rect(surface, "red", sprite.get_hitbox(), 1)


def draw_grid(surface):
    """Vẽ các ô lưới lên surface nhận vào"""
    cols = int(surface.get_width() / (BLOCK_SIZE * SCALE))
    rows = int(surface.get_height() / (BLOCK_SIZE * SCALE))
    for r in range(rows):
        for c in range(cols):
            cell = pygame.Rect(c * BLOCK_SIZE * SCALE, r * BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
            pygame.draw.rect(surface, "red", cell, 1)
