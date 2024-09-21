
from utils.spriteLoader import SpriteLoader


class Button():
    def __init__(self, text, default_color, hovered_color, topleft):
        self.default_img = SpriteLoader().text_image(text, default_color)
        self.hovered_img = SpriteLoader().text_image(text, hovered_color)
        self.topleft = topleft

        self.image = self.default_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.frame_count = 0
        self.frame_rate = 10
        self.is_hovered = False

    def draw(self, surface):
        self.rect = self.image.get_rect(topleft = self.topleft)
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        mouse_pos = event.pos
        mouse_clicked = event.button == 1
        return self.rect.collidepoint(mouse_pos) and mouse_clicked
    
    def update(self):
        self.frame_count += 1
        if(self.frame_count >= self.frame_rate):
            if(self.is_hovered):
                self.image = self.hovered_img
                self.is_hovered = False
            else:
                self.image = self.default_img
                self.is_hovered = True
            self.frame_count = 0

    def reset(self):
        self.image = self.default_img
        self.is_hovered = False

    def handle_clicked(): pass
