import pygame.transform
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT, SCALE
from src.utils.image_loader import ImageLoader
from src.scenes.component import TextButton

class GameOver(Scene):
    """Màn hình Game Over"""

    def __init__(self, game):
        super().__init__(game)
        self.__title = pygame.transform.scale_by(ImageLoader().text_image("Game Over", "red"), 2)
        self.__score_label = ImageLoader().text_image("Score", "cyan")
        self.__highest_score_label = ImageLoader().text_image("Highest Score", "cyan")
        self.__time_label = ImageLoader().text_image("Time", "cyan")

        # Định nghĩa hành động cho các nút
        self.__button_play_again = TextButton("Play Again", action=lambda: self._game.switch_scene("GamePlay"))
        self.__button_main_menu = TextButton("Main Menu", action=lambda: self._game.switch_scene("MainMenu"))

        self.__buttons = [self.__button_play_again, self.__button_main_menu]
        self.__selected_button = 0  # Chỉ số của nút hiện tại được chọn

        # Dữ liệu mẫu để hiển thị
        self.__score = ImageLoader().text_image("750")  # Dữ liệu thử nghiệm
        self.__highest_score = ImageLoader().text_image("1000")  # Dữ liệu thử nghiệm
        self.__time = ImageLoader().text_image("15'30")  # Dữ liệu thử nghiệm

        self.render_surface()

    def render_surface(self):
        """Vẽ màn hình Game Over"""
        self._surface.fill((0, 0, 0))  # Xóa màn hình với màu đen

        # render title "GAME OVER"
        position = (WIDTH / 2, HEIGHT / 2 - 100 * SCALE)
        rect = self.__title.get_rect(center=position)
        self._surface.blit(self.__title, rect)

        # render label "SCORE"
        position = (WIDTH/2 - 150 * SCALE, HEIGHT/2 - 70 * SCALE)
        self._surface.blit(self.__score_label, self.__score_label.get_rect(center=position))
        self._surface.blit(self.__score, self.__score.get_rect(center=(position[0], position[1] + 10 * SCALE)))

        # render label "HIGHEST SCORE"
        position = (WIDTH/2, HEIGHT/2 - 70 * SCALE)
        self._surface.blit(self.__highest_score_label, self.__highest_score_label.get_rect(center=position))
        self._surface.blit(self.__highest_score, self.__highest_score.get_rect(center=(position[0], position[1] + 10 * SCALE)))

        # render label "TIME"
        position = (WIDTH/2 + 150 * SCALE, HEIGHT/2 - 70 * SCALE)
        self._surface.blit(self.__time_label, self.__time_label.get_rect(center=position))
        self._surface.blit(self.__time, self.__time.get_rect(center=(position[0], position[1] + 10 * SCALE)))

        # render buttons
        self.__button_play_again.set_position(center=(WIDTH/2, HEIGHT/2))
        self.__button_play_again.render(self._surface)

        self.__button_main_menu.set_position(center=(WIDTH / 2, HEIGHT / 2 + self.__button_main_menu.get_height() + 20 * SCALE))
        self.__button_main_menu.render(self._surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.__selected_button = (self.__selected_button - 1) % len(self.__buttons)
            elif event.key == pygame.K_DOWN:
                self.__selected_button = (self.__selected_button + 1) % len(self.__buttons)
            elif event.key == pygame.K_RETURN:  # Nhấn Enter để chọn nút
                self.__buttons[self.__selected_button].action()  # Gọi hành động của nút

    def update(self):
        for index, button in enumerate(self.__buttons):
            button.blur()  # Mờ tất cả các nút
            if index == self.__selected_button:
                button.focus()  # Tập trung vào nút đang được chọn
                button.update()  # Cập nhật hiệu ứng nhấp nháy cho nút

        self.render_surface()

    def reset(self):
        self.__selected_button = 0
