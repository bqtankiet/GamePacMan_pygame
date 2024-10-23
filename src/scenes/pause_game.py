import pygame.transform

from src.scenes.component import TextButton
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT, SCALE
from src.utils.image_loader import ImageLoader


class PauseGame(Scene):
    """Màn hình PauseGame"""

    def __init__(self, game):
        super().__init__(game)
        self.__title = pygame.transform.scale_by(ImageLoader().text_image("Pause Game", "yellow"), 2)
        self.__button_resume = TextButton("Resume", action=lambda: print("Resume clicked"))
        self.__button_main_menu = TextButton("Main Menu", action=lambda: print("Main Menu clicked"))

        self.render_surface()

    #-----------------------------------------
    # Các methods override của lớp cha (Scene)
    #-----------------------------------------
    def render_surface(self):
        # render title
        title_rect = self.__title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100 * SCALE))
        self._surface.blit(self.__title, title_rect)

        # render button "Resume"
        position = (WIDTH/2, HEIGHT/2)
        self.__button_resume.set_position(center = position)
        self.__button_resume.render(self._surface)

        # render button "Main Menu"
        position = (WIDTH / 2, HEIGHT / 2 + self.__button_main_menu.get_height() + 20 * SCALE)
        self.__button_main_menu.set_position(center = position)
        self.__button_main_menu.render(self._surface)

    def handle_event(self, event):
        # TODO: Xử lý khi nhấn mũi tên xuống
        # TODO: Xử lý khi nhấn mũi tên lên
        # TODO: Xử lý khi nhấn enter
        pass

    def update(self):
        # TODO: Xử lý cập nhật màn hình PauseGame sau mỗi frame
        # TODO: Xử lý để button đang chọn có thể nhấp nháy
        pass

    def reset(self):
        pass

    #----------------------------------------
    # Các methods riêng của lớp
    #----------------------------------------
