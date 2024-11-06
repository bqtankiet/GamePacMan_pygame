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
                self.__button_group.current().fire()
            elif event.key == pygame.K_DOWN:
                self.__button_group.next()
            elif event.key == pygame.K_UP:
                self.__button_group.previous()

    def update(self):
        self.__button_group.update() # Cập nhật lại trạng thái các button
        self.render_surface() # Cập nhật lại giao diện

    def reset(self):
        self.__button_group.reset()
