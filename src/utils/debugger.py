import pygame


def draw_hitbox(surface, sprite):
    pygame.draw.rect(surface, "red", sprite.get_hitbox(), 1)