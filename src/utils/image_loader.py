import pygame

from .constant import SCALE
IMAGE_FOLDER = "../resource/images/"

class ImageLoader:
    """Singleton"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.general_sprites = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - General Sprites.png").convert_alpha()
            self.scene = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - Attract Mode & HUD Assets.png").convert_alpha()
            self.all_text = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - Text.png").convert_alpha()
            self.initialized = True

    # Background
    def background_main_menu(self):
        img = self.scene.subsurface(464, 304, 224, 288)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    # Fruits
    def cherry(self):
        img = self.general_sprites.subsurface(488, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def straw_berry(self):
        img = self.general_sprites.subsurface(504, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def orange(self):
        img = self.general_sprites.subsurface(520, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def apple(self):
        img = self.general_sprites.subsurface(536, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def melon(self):
        img = self.general_sprites.subsurface(552, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def galaxian(self):
        img = self.general_sprites.subsurface(568, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def bell(self):
        img = self.general_sprites.subsurface(584, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def key(self):
        img = self.general_sprites.subsurface(600, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    # Score
    def score_100(self):
        img = self.general_sprites.subsurface(456, 144, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def score_200(self):
        img = self.general_sprites.subsurface(456, 128, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def score_300(self):
        img = self.general_sprites.subsurface(472, 144, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def score_400(self):
        img = self.general_sprites.subsurface(472, 128, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def score_500(self):
        img = self.general_sprites.subsurface(488, 144, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def score_700(self):
        img = self.general_sprites.subsurface(504, 144, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def score_800(self):
        img = self.general_sprites.subsurface(488, 128, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def score_1600(self):
        img = self.general_sprites.subsurface(504, 128, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    # Pacman
    def pacman_live(self):
        img = self.general_sprites.subsurface(584, 16, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    # Text
    def text_image(self, text, color = 'white'):
        text = text.upper()
        text_surface = pygame.Surface((len(text)*8, 8))
        for index, char in enumerate(text):
            if   char in "ABCDEFGHIJKLMNO": pos = {'line': 0, 'index': ord(char) - ord('A')}
            elif char in "PQRSTUVWXYZ":     pos = {'line': 1, 'index': ord(char) - ord('P')}
            elif char in "0123456789":      pos = {'line': 2, 'index': ord(char) - ord('0')}
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
    
