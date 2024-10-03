import pygame

from src.utils.constant import HEIGHT, SCALE, WIDTH
from src.utils.image_loader import ImageLoader


class TextButton:
    def __init__(self, text, default_color, hovered_color, top_left=(0, 0)):
        image_loader = ImageLoader()
        self.rect = None
        self.default_img = image_loader.text_image(text, default_color)
        self.hovered_img = image_loader.text_image(text, hovered_color)
        self.top_left = top_left

        self.image = self.default_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.frame_count = 0
        self.frame_rate = 10
        self.is_hovered = False

    def render(self, surface):
        self.rect = self.image.get_rect(topleft=self.top_left)
        surface.blit(self.image, self.rect)

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_rate:
            if self.is_hovered:
                self.image = self.hovered_img
                self.is_hovered = False
            else:
                self.image = self.default_img
                self.is_hovered = True
            self.frame_count = 0

    def reset(self):
        self.image = self.default_img
        self.is_hovered = False

    def handle_clicked(self): pass


class ButtonFactory:
    @staticmethod
    def create_btn_start_game():
        top_left = ((WIDTH - 80 * SCALE) // 2, 220)
        return TextButton("Start Game", "white", "red", top_left)

    @staticmethod
    def create_btn_exit():
        top_left = ((WIDTH - 40 * SCALE) // 2, 270)
        return TextButton("Exit", "white", "red", top_left)
