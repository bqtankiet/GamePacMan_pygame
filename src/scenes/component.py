from src.utils.image_loader import ImageLoader


class TextButton:
    def __init__(self, text, *, action=None):
        self.__default_img = ImageLoader().text_image(text, "white")
        self.__hovered_img = ImageLoader().text_image(text, "red")
        self.__image = self.__default_img
        self.__rect = self.__image.get_rect()

        self.action = action

        self.frame_count = 0
        self.frame_rate = 10
        self.is_focused = False

    def set_position(self, **kwargs):
        if "top_left" in kwargs:
            self.__rect.topleft = kwargs['top_left']
        elif "center" in kwargs:
            self.__rect.center = kwargs['center']

    def get_width(self):
        return self.__image.get_width()

    def get_height(self):
        return self.__image.get_height()

    def render(self, surface):
        surface.blit(self.__image, self.__rect)

    def update(self):
        """Phương thức này để tạo hiệu ứng nhấp nháy khi nó đang được focus"""
        if not self.is_focused: return
        self.frame_count += 1
        if self.frame_count < self.frame_rate:
            self.__image = self.__hovered_img
        elif self.frame_count < self.frame_rate*2:
            self.__image = self.__default_img
        else:
            self.frame_count = 0


    def focus(self):
        self.is_focused = True
        self.__image = self.__hovered_img

    def blur(self):
        self.is_focused = False
        self.__image = self.__default_img

    def fire(self):
        if self.action:
            print(f"Action for '{self.__rect}' triggered.")  # Thêm log
            self.action()

class ButtonGroup:
    def __init__(self, buttons):
        self.__buttons = buttons
        self.__index = 0

    def current(self):
        return self.__buttons[self.__index]

    def next(self):
        self.__index = (self.__index + 1) % len(self.__buttons)
        return self.__buttons[self.__index]

    def previous(self):
        self.__index = (self.__index - 1) % len(self.__buttons)
        return self.__buttons[self.__index]

    def reset(self):
        # Đặt về nút ban đầu và làm mờ các nút
        self.__index = 0
        for button in self.__buttons:
            button.blur()

    def update(self):
        for button in self.__buttons: # Mờ tất cả các nút
            button.blur()
        self.current().focus() # Tập trung vào nút đang được chọn
        self.current().update() # Cập nhật hiệu ứng nhấp nháy cho nút