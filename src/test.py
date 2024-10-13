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
            box1 = pygame.Surface((50, 50))
            box1.fill("red")
            box1_rect = box1.get_rect(topleft=(0, 0))

            box2 = pygame.Surface((50, 50))
            box2.fill("green")
            box2_rect = box2.get_rect(topleft = (0, 50))

            screen.blit(box1, box1_rect.topleft)
            screen.blit(box2, box2_rect.topleft)
            print(box1_rect, box2_rect)
            print(box1_rect.colliderect(box2_rect))

            # end update
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()
