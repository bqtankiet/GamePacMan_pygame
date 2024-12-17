import pygame.transform
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT, SCALE
from src.utils.image_loader import ImageLoader
from src.scenes.component import TextButton, ButtonGroup
import src.core.game as g


class GameOver(Scene):
    """Màn hình Game Over"""

    def __init__(self):
        super().__init__()
        self._game = g.Game.get_instance()
        # Định nghĩa các label
        self.__title = pygame.transform.scale_by(ImageLoader().text_image("Game Over", "red"), 2)
        self.__score_label = ImageLoader().text_image("Score", "cyan")
        self.__highest_score_label = ImageLoader().text_image("Highest Score", "cyan")
        self.__time_label = ImageLoader().text_image("Time", "cyan")

        # Định nghĩa hành động cho các nút
        self.__button_play_again = TextButton("Play Again", action=lambda: self._game.switch_scene("GamePlay", reset = True))
        self.__button_main_menu = TextButton("Main Menu", action=lambda: self._game.switch_scene("MainMenu"))

        # ButtonGroup để quản lý các nút
        self.__button_group = ButtonGroup([self.__button_play_again, self.__button_main_menu])

        # Dữ liệu mẫu để hiển thị
        self.__score = ImageLoader().text_image("750")  # Dữ liệu thử nghiệm
        self.__highest_score = ImageLoader().text_image("1000")  # Dữ liệu thử nghiệm
        self.__time = ImageLoader().text_image("15'30")  # Dữ liệu thử nghiệm

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
                self.__button_group.previous()
            elif event.key == pygame.K_DOWN:
                self.__button_group.next()
            elif event.key == pygame.K_RETURN:  # Nhấn Enter để chọn nút
                self.__button_group.current().fire()

    def update(self):
        self.__button_group.update() # Cập nhật lại trạng thái các button

    def reset(self): pass

    def on_enter(self):
        self.__button_group.reset()

        # render status: score, highest_score, time
        current_time = self._game.game_status.current_time()
        score = self._game.game_status.current_score()
        highest_score = self._game.game_status.highest_score()
        self.__score = ImageLoader().text_image(f'{score}')
        self.__highest_score = ImageLoader().text_image(f'{highest_score}')
        self.__time = ImageLoader().text_image(f"{current_time[0]}'{current_time[1]:02}")


