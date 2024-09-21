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
            self.general_sprites = pygame.image.load(RESOURCE + "Arcade - Pac-Man - General Sprites.png")
            self.scene = pygame.image.load(RESOURCE + "Arcade - Pac-Man - Attract Mode & HUD Assets.png")
            self.text = pygame.image.load(RESOURCE + "text.png")
            self.all_text = pygame.image.load(RESOURCE + "Arcade - Pac-Man - Text.png")
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

    def text_image(self, text, color = 'white'):
        text = text.upper()
        text_surface = pygame.Surface((len(text)*8, 8))
        index = 0
        for char in text:
            if char == " ": 
                index+=1
                continue

            if(char in "ABCDEFGHIJKLMNO"):  pos = {'line': 0, 'index': ord(char) - ord('A')}
            if(char in "PQRSTUVWXYZ"):      pos = {'line': 1, 'index': ord(char) - ord('P')}
            if(char in "0123456789"):       pos = {'line': 2, 'index': ord(char) - ord('0')}
            if(color.lower() == "red"):     pos["line"] += 4
            if(color.lower() == "pink"):    pos["line"] += 4*2
            if(color.lower() == "cyan"):    pos["line"] += 4*3
            if(color.lower() == "orange"):  pos["line"] += 4*4
            if(color.lower() == "yellow"):  pos["line"] += 4*6

            left_top = (pos["index"]*8, pos["line"]*8)
            char_img = self.all_text.subsurface(left_top, (8, 8))
            text_surface.blit(char_img, (index*8, 0))
            index += 1

        text_surface = pygame.transform.scale_by(text_surface, SCALE)
        return text_surface
    
