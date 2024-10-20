import pygame

from src.utils.constant import WIDTH, HEIGHT
from src.utils.image_loader import ImageLoader

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # update
            image = ImageLoader().text_image("Hello World")
            screen.blit(image, (100, 100))

            # end update
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()
