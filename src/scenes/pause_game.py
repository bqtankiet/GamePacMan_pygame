import pygame.transform

from src.scenes.component import TextButton, ButtonGroup
from src.scenes.scene import Scene
from src.utils.constant import WIDTH, HEIGHT, SCALE
from src.utils.image_loader import ImageLoader


class PauseGame(Scene):
    """Màn hình PauseGame"""

    def __init__(self, game):
        super().__init__(game)
        # Định nghĩa các label
        self.__title = pygame.transform.scale_by(ImageLoader().text_image("Pause Game", "yellow"), 2)
        self.__score_label = ImageLoader().text_image(" Current score", "cyan")
        self.__highest_score_label = ImageLoader().text_image("Highest Score", "cyan")
        self.__time_label = ImageLoader().text_image("Time", "cyan")

        # Định nghĩa hành động cho các button
        self.__button_resume = TextButton("Resume", action=lambda: self._game.switch_scene("GamePlay"))
        self.__button_main_menu = TextButton("Main Menu", action=lambda: self._game.switch_scene("MainMenu"))

        # ButtonGroup để quản lý các nút
        self.__button_group = ButtonGroup([self.__button_resume, self.__button_main_menu])

        # Tạo dữ liệu mẫu để test
        self.__score = ImageLoader().text_image("750") # TODO: Dữ liệu chỉ để test
        self.__highest_score = ImageLoader().text_image("1000") # TODO: Dữ liệu chỉ để test
        self.__time = ImageLoader().text_image("15'30") # TODO: Dữ liệu chỉ để test


    #-----------------------------------------
    # Các methods override của lớp cha (Scene)
    #-----------------------------------------
    def render_surface(self):
        # render title
        title_rect = self.__title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 100 * SCALE))
        self._surface.blit(self.__title, title_rect)

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

        # render button "Resume"
        position = (WIDTH/2, HEIGHT/2)
        self.__button_resume.set_position(center = position)
        self.__button_resume.render(self._surface)

        # render button "Main Menu"
        position = (WIDTH / 2, HEIGHT / 2 + self.__button_main_menu.get_height() + 20 * SCALE)
        self.__button_main_menu.set_position(center = position)
        self.__button_main_menu.render(self._surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.__button_group.next()
            elif event.key == pygame.K_UP:
                self.__button_group.previous()
            elif event.key == pygame.K_RETURN:
                self.__button_group.current().fire()

    def update(self):
        self.__button_group.update() # Cập nhật lại trạng thái các button
        self.render_surface() # Cập nhật lại giao diện

    def reset(self):
        self.__button_group.reset()

    #----------------------------------------
    # Các methods riêng của lớp
    #----------------------------------------
