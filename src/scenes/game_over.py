import pygame.transform
from pygame.transform import scale_by

from src.scenes.component import TextButton
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT, SCALE
from src.utils.image_loader import ImageLoader


class GameOver(Scene):
    """Màn hình PauseGame"""

    def __init__(self, game):
        super().__init__(game)
        self.__title = pygame.transform.scale_by(ImageLoader().text_image("Game Over", "red"), 2)
        self.__score_label = ImageLoader().text_image("Score", "cyan")
        self.__highest_score_label = ImageLoader().text_image("Highest Score", "cyan")
        self.__time_label = ImageLoader().text_image("Time", "cyan")
        self.__button_play_again = TextButton("Play Again", action=lambda: print("Play Again clicked"))
        self.__button_main_menu = TextButton("Main Menu", action=lambda: print("Main Menu clicked"))
        # ---
        self.__score = ImageLoader().text_image("750") # TODO: Dữ liệu chỉ để test
        self.__highest_score = ImageLoader().text_image("1000") # TODO: Dữ liệu chỉ để test
        self.__time = ImageLoader().text_image("15'30") # TODO: Dữ liệu chỉ để test
        # ---
        self.render_surface()

    #-----------------------------------------
    # Các methods override của lớp cha (Scene)
    #-----------------------------------------
    def render_surface(self):
        # render title "GAME OVER"
        position = (WIDTH / 2, HEIGHT / 2 - 100 * SCALE)
        rect = self.__title.get_rect(center=position)
        self._surface.blit(self.__title, rect)

        # render label "SCORE"
        position = (WIDTH/2 - 150 * SCALE, HEIGHT/2 - 70 * SCALE)
        rect = self.__score_label.get_rect(center=position)
        self._surface.blit(self.__score_label, rect)

        rect = self.__score.get_rect(center=position)
        rect = rect.move(0, 10*SCALE)
        self._surface.blit(self.__score, rect)

        # render label "HIGHEST SCORE"
        position = (WIDTH/2, HEIGHT/2 - 70 * SCALE)
        rect = self.__highest_score_label.get_rect(center=position)
        self._surface.blit(self.__highest_score_label, rect)

        rect = self.__highest_score.get_rect(center=position)
        rect = rect.move(0, 10*SCALE)
        self._surface.blit(self.__highest_score, rect)

        # render label "TIME"
        position = (WIDTH/2 + 150 * SCALE, HEIGHT/2 - 70 * SCALE)
        rect = self.__time_label.get_rect(center=position)
        self._surface.blit(self.__time_label, rect)

        rect = self.__time.get_rect(center=position)
        rect = rect.move(0, 10*SCALE)
        self._surface.blit(self.__time, rect)

        # render button "PLAY AGAIN"
        position = (WIDTH/2, HEIGHT/2)
        self.__button_play_again.set_position(center = position)
        self.__button_play_again.render(self._surface)

        # render button "MAIN MENU"
        position = (WIDTH / 2, HEIGHT / 2 + self.__button_main_menu.get_height() + 20 * SCALE)
        self.__button_main_menu.set_position(center = position)
        self.__button_main_menu.render(self._surface)

    def handle_event(self, event):
        # TODO: Xử lý khi nhấn mũi tên xuống
        # TODO: Xử lý khi nhấn mũi tên lên
        # TODO: Xử lý khi nhấn enter
        pass

    def update(self):
        # TODO: Xử lý cập nhật màn hình GameOver sau mỗi frame
        # TODO: Xử lý để button đang chọn có thể nhấp nháy
        pass

    def reset(self):
        pass

    #----------------------------------------
    # Các methods riêng của lớp
    #----------------------------------------
