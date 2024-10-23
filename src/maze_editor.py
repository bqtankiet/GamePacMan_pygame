import pygame

from src.entities.maze import Maze
from src.utils.constant import WIDTH, HEIGHT, BLOCK_SIZE, SCALE
from src.utils.debugger import draw_grid


class MazeEditor:
    def __init__(self): pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    running = True
    maze = Maze()
    cols = int(maze.image.get_width() / (BLOCK_SIZE * SCALE))
    rows = int(maze.image.get_height() / (BLOCK_SIZE * SCALE))
    grid = [[0 for i in range(cols)] for j in range(rows)]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                r = int(pos[1] / (BLOCK_SIZE * SCALE))
                c = int(pos[0] / (BLOCK_SIZE * SCALE))
                if pygame.mouse.get_pressed()[0]:
                    grid[r][c] = 1
                    pygame.draw.rect(screen, "red",
                                     pygame.Rect(c * BLOCK_SIZE * SCALE, r * BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE,
                                                 BLOCK_SIZE * SCALE))
                if pygame.mouse.get_pressed()[2]:
                    grid[r][c] = 0

            # update
            screen.blit(maze.image, (0, 0))
            draw_grid(maze.image)
            # end update
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()
    for r in range(rows):
        print(f"{grid[r]},")
