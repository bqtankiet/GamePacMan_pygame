from src.utils.constant import BLOCK_SIZE, SCALE

block_size_scaled = BLOCK_SIZE * SCALE

def pixel_to_grid(position):
    """Chuyển đổi pixel thành vị trí trong lưới"""
    x, y = position
    r = int(y / block_size_scaled)
    c = int(x / block_size_scaled)
    return r, c


def grid_to_pixel(position):
    """Chuyển đổi vị trí ô trong lưới sang vị trí pixel"""
    x = (position[1] * block_size_scaled) + (block_size_scaled / 2)
    y = (position[0] * block_size_scaled) + (block_size_scaled / 2)
    return x, y