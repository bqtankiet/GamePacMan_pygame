import pygame

from utils.constant import SCALE
IMAGE_FOLDER = "resource/images/"

class ImageLoader:
    """Singleton"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.general_sprites = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - General Sprites.png")
            self.scene = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - Attract Mode & HUD Assets.png")
            self.all_text = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - Text.png")
            self.initialized = True
    
    def background_main_menu (self):
        img = self.scene.subsurface(464, 304, 224, 288)
        img = pygame.transform.scale_by(img, SCALE)
        return img
    
    def text_image(self, text, color = 'white'):
        text = text.upper()
        text_surface = pygame.Surface((len(text)*8, 8))
        for index, char in enumerate(text):
            if  (char in "ABCDEFGHIJKLMNO"):pos = {'line': 0, 'index': ord(char) - ord('A')}
            elif(char in "PQRSTUVWXYZ"):    pos = {'line': 1, 'index': ord(char) - ord('P')}
            elif(char in "0123456789"):     pos = {'line': 2, 'index': ord(char) - ord('0')}
            else: continue #Nếu không phải 'chữ' hoặc 'số' thì duyệt qua kí tự tiếp theo
            
            match(color.lower()):
                case "red":     pos["line"] += 4
                case "pink":    pos["line"] += 4*2
                case "cyan":    pos["line"] += 4*3
                case "orange":  pos["line"] += 4*4
                case "yellow":  pos["line"] += 4*6
                
            left_top = (pos["index"]*8, pos["line"]*8)
            char_img = self.all_text.subsurface(left_top, (8, 8))
            text_surface.blit(char_img, (index*8, 0))

        text_surface = pygame.transform.scale_by(text_surface, SCALE)
        return text_surface
    
