import pygame.draw

from src.utils.constant import BLOCK_SIZE, SCALE

"""Module phục vụ cho việc debug"""
ghost_paths = {
    'ghost_red': 'path_red',
    'ghost_orange': 'path_orange',
    'ghost_cyan': 'path_cyan',
    'ghost_pink': 'path_pink'
}

attributes = {}
mode = None

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

def draw_path(surface, path, color):
    if not path: return
    for n in path:
        c, r = n.position
        cell = pygame.Rect(c * BLOCK_SIZE * SCALE, r * BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        pygame.draw.rect(surface, color, cell, 1)

def render(surface):
    if mode is None: return
    match mode:
        case "f1": draw_grid(surface)
        case "f2": draw_hitbox(surface, get_attributes('hitbox'))
        case "f3":
            draw_path(surface, get_attributes('path_red'), "red")
            draw_path(surface, get_attributes('path_orange'), "orange")
            draw_path(surface, get_attributes('path_pink'), "pink")
            draw_path(surface, get_attributes('path_cyan'), "cyan")


def toggle_mode(m):
    global mode
    if mode == m: mode = None
    else: mode = m

def handle_event(event):
    if event.type != pygame.KEYDOWN: return
    if event.key == pygame.K_F1: toggle_mode('f1')
    elif event.key == pygame.K_F2: toggle_mode('f2')
    elif event.key == pygame.K_F3: toggle_mode('f3')

def set_attributes(key, attr):
    attributes[key] = attr

def get_attributes(key):
    if key in attributes: return attributes[key]
