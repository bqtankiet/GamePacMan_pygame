
import sys

import pygame

from src.scenes.component import ButtonFactory
from src.scenes.scene import Scene
from src.utils.constant import HEIGHT, WIDTH
from src.utils.image_loader import ImageLoader


class MainMenu(Scene):

    def __init__(self, game):
        super().__init__(game)
        self.button_start_game = None
        self.button_exit = None
        self.selected_button = None
        self.render_surface()

    def render_surface(self):
        """Override Scene.render_surface"""
        image_loader = ImageLoader()
        # background
        background = image_loader.background_main_menu()
        self.surface.blit(background, background.get_rect(center = (WIDTH // 2, HEIGHT // 2)))

        # text button "START GAME"
        self.button_start_game = ButtonFactory.create_btn_start_game()
        self.button_start_game.render(self.surface)
        self.button_start_game.handle_clicked = self.__handle_start_game_clicked

        # text button "EXIT"
        self.button_exit = ButtonFactory.create_btn_exit()
        self.button_exit.render(self.surface)
        self.button_exit.handle_clicked = self.__handle_exit_clicked

        # selected button
        self.selected_button = self.button_start_game

    def handle_event(self):
        """Override Scene.handle_event"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.selected_button.handle_clicked()
        elif keys[pygame.K_UP]:
            self.__reset_button(self.button_exit)
            self.selected_button = self.button_start_game
        elif keys[pygame.K_DOWN]:
            self.__reset_button(self.button_start_game)
            self.selected_button = self.button_exit

    def update(self):
        """Override Scene.update"""
        self.selected_button.update()
        self.selected_button.render(self.surface)

    def reset(self): pass

    # các method cụ thể để xử lý sự kiện của button cụ thể 
    def __handle_start_game_clicked(self):
        print("Start Game Clicked - scenes.main_menu.handle_start_game_clicked")
        # Todo: Thay đổi current_scene của GameManger sang màn hình GamePlay
        self.game.switch_scene("GamePlay")

    def __handle_exit_clicked(self):
        print("Exit Clicked - scenes.main_menu.handle_exit_clicked")
        self.game.running = False

    def __reset_button(self, button):
        button.reset()
        button.render(self.surface)

