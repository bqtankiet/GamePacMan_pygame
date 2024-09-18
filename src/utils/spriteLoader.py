import pygame

from utils.constant import SCALE
RESOURCE = "resource/sprites/"

class SpriteLoader:
    """Singleton"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpriteLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.general_sprites = pygame.image.load(RESOURCE + "general_sprites.png")
            self.scene = pygame.image.load(RESOURCE + "scene.png")
            self.text = pygame.image.load(RESOURCE + "text.png")
            self.initialized = True
    
    def background_main_menu (self):
        img = self.scene.subsurface(pygame.Rect(464, 304, 224, 288))
        img = pygame.transform.scale_by(img, SCALE)
        return img
    
    def text_start_game_white (self):
        img = self.text.subsurface(pygame.Rect(8,8,80,8))
        img = pygame.transform.scale_by(img, SCALE)
        return img
    
    def text_start_game_cyan (self):
        img = self.text.subsurface(pygame.Rect(8,24,80,8))
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def text_exit_white(self):
        img = self.text.subsurface(pygame.Rect(8,40,32,8))
        img = pygame.transform.scale_by(img, SCALE)
        return img
    
    def text_exit_cyan(self):
        img = self.text.subsurface(pygame.Rect(8,56,32,8))
        img = pygame.transform.scale_by(img, SCALE)
        return img

