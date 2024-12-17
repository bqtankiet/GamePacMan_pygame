import pygame

from .constant import SCALE

IMAGE_FOLDER = "../resource/images/"


class ImageLoader:
    """Singleton. Quản lý các hình ảnh của game. Cung cấp các phương thức để lấy hình ảnh"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageLoader, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.initialized = True
            # load sprite image
            self.general_sprites = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - General Sprites.png")
            self.scene = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - Attract Mode & HUD Assets.png")
            self.all_text = pygame.image.load(IMAGE_FOLDER + "Arcade - Pac-Man - Text.png")
            # remove background
            self.general_sprites.set_colorkey((0, 0, 0))
            self.all_text.set_colorkey((0, 0, 0))
            self.scene.set_colorkey((0, 0, 0))

    # Background
    def background_main_menu(self):
        img = self.scene.subsurface(464, 304, 224, 288)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def background_maze(self):
        img = self.general_sprites.subsurface(0, 0, 224, 248)
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

    def pacman_0(self):
        img = self.general_sprites.subsurface(488, 0, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_r1(self):
        img = self.general_sprites.subsurface(472, 0, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_r2(self):
        img = self.general_sprites.subsurface(456, 0, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_l1(self):
        img = self.general_sprites.subsurface(472, 16, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_l2(self):
        img = self.general_sprites.subsurface(456, 16, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_u1(self):
        img = self.general_sprites.subsurface(472, 32, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_u2(self):
        img = self.general_sprites.subsurface(456, 32, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_d1(self):
        img = self.general_sprites.subsurface(472, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_d2(self):
        img = self.general_sprites.subsurface(456, 48, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img



    # Ghost
    def ghost(self, color, direction):
        y_index = -1
        if color == 'red': y_index = 0
        if color == 'pink': y_index = 1
        if color == 'cyan': y_index = 2
        if color == 'orange': y_index = 3

        x_index = -1
        if direction == 'r1': x_index = 0
        if direction == 'r2': x_index = 1
        if direction == 'l1': x_index = 2
        if direction == 'l2': x_index = 3
        if direction == 'u1': x_index = 4
        if direction == 'u2': x_index = 5
        if direction == 'd1': x_index = 6
        if direction == 'd2': x_index = 7

        img = self.general_sprites.subsurface(456+(16*x_index), 64+(16*y_index), 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def frightened_1(self, color = 'normal'):
        img = None
        if color == 'normal' or color is None:
            img = self.general_sprites.subsurface(584, 64, 16, 16)
        elif color == 'white':
            img = self.general_sprites.subsurface(616, 64, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def frightened_2(self, color = 'normal'):
        img = None
        if color == 'normal' or color is None:
            img = self.general_sprites.subsurface(600, 64, 16, 16)
        elif color == 'white':
            img = self.general_sprites.subsurface(632, 64, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    def pacman_dead(self, index):
        if 0 <= index <= 11:
            img = self.general_sprites.subsurface(488+(16*index), 0, 16, 16)
            img = pygame.transform.scale_by(img, SCALE)
            return img
        return None

    def ghost_dead(self, direction):
        index = 0
        if   direction == 'right': index = 0
        elif direction == 'left': index = 1
        elif direction == 'up': index = 2
        elif direction == 'down': index = 3
        img = self.general_sprites.subsurface(584+(16*index), 80, 16, 16)
        img = pygame.transform.scale_by(img, SCALE)
        return img

    # Text
    def text_image(self, text, color='white'):
        text = text.upper()
        text_surface = pygame.Surface((len(text) * 8, 8))
        for index, char in enumerate(text):
            if char in "ABCDEFGHIJKLMNO":
                pos = {'line': 0, 'index': ord(char) - ord('A')}
            elif char in "PQRSTUVWXYZ":
                pos = {'line': 1, 'index': ord(char) - ord('P')}
            elif char in "0123456789":
                pos = {'line': 2, 'index': ord(char) - ord('0')}
            elif char in "'":
                pos = {'line': 2, 'index': 12}
            elif char in "!":
                pos = {'line': 1, 'index': 11}
            else:
                continue  # Nếu không phải 'chữ' hoặc 'số' thì duyệt qua kí tự tiếp theo

            match (color.lower()):
                case "red":
                    pos["line"] += 4
                case "pink":
                    pos["line"] += 4 * 2
                case "cyan":
                    pos["line"] += 4 * 3
                case "orange":
                    pos["line"] += 4 * 4
                case "yellow":
                    pos["line"] += 4 * 6

            left_top = (pos["index"] * 8, pos["line"] * 8)
            char_img = self.all_text.subsurface(left_top, (8, 8))
            text_surface.blit(char_img, (index * 8, 0))

        text_surface = pygame.transform.scale_by(text_surface, SCALE)
        return text_surface
