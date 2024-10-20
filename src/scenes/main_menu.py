import pygame

from src.scenes.component import TextButton, ButtonGroup
from src.scenes.scene import Scene
from src.utils.constant import HEIGHT, WIDTH, SCALE
from src.utils.image_loader import ImageLoader


class MainMenu(Scene):
    """Màn hình Main Menu của game """

    def __init__(self, game):
        super().__init__(game)
        self.__background = ImageLoader().background_main_menu()
        self.__button_start = TextButton("Start Game", action=lambda: self._game.switch_scene("GamePlay"))
        self.__button_exit = TextButton("Exit", action=lambda: self._game.exit())
        self.__button_group = ButtonGroup([self.__button_start, self.__button_exit])

        self.__selected_button = self.__button_group.current()
        self.__selected_button.focus()

        self.render_surface()

    #-----------------------------------------
    # Các methods override của lớp cha (Scene)
    #-----------------------------------------
    def render_surface(self):
        # render background
        background_rect = self.__background.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self._surface.blit(self.__background, background_rect)

        # render button "START GAME"
        position = (WIDTH // 2, background_rect.y + 60*SCALE)
        self.__button_start.set_position(center=position)
        self.__button_start.render(self._surface)

        # render button "EXIT"
        position = (WIDTH // 2, background_rect.y + 80*SCALE)
        self.__button_exit.set_position(center=position)
        self.__button_exit.render(self._surface)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.enter()
            elif event.key == pygame.K_DOWN:
                self.navigate(1)
            elif event.key == pygame.K_UP:
                self.navigate(-1)

    def update(self):
        self.__selected_button.update()
        self.render_surface()

    def reset(self):
        pass

    #----------------------------------------
    # Các methods riêng của lớp MainMenu
    #----------------------------------------
    def navigate(self, direction):
        # Xóa focus cũ
        self.__selected_button.blur()

        # chọn button mới
        if direction > 0:
            self.__button_group.next()
        elif direction < 0:
            self.__button_group.previous()
        self.__selected_button = self.__button_group.current()

        # Focus vào button đang chọn
        self.__selected_button.focus()

    def enter(self):
        self.__selected_button.fire()
