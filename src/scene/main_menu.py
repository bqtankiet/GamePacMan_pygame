import sys
import pygame
from component.button_factory import ButtonFactory
from utils.constant import HEIGHT, SCALE, WIDTH
from utils.spriteLoader import SpriteLoader
from .scene import Scene


class MainMenu(Scene):

    def renderSurface(self):
        """Override Scene.renderSurface"""
        spriteLoader = SpriteLoader()
        # background
        background = spriteLoader.background_main_menu()
        self._surface.blit(background, background.get_rect(center = (WIDTH//2, HEIGHT//2)))

        # text button "START GAME"
        button_position = ((WIDTH-80*SCALE)//2, 220)
        self.button_start_game = ButtonFactory.create_btn_start_game(button_position)
        self.button_start_game.draw(self._surface)
        self.button_start_game.handle_clicked = self.__handle_start_game_clicked

        # text button "EXIT"
        button_position = (((WIDTH-40*SCALE)//2, 270))
        self.button_exit = ButtonFactory.create_btn_exit(button_position)
        self.button_exit.draw(self._surface)
        self.button_exit.handle_clicked = self.__handle_exit_clicked

        # selected button
        self.selected_button = self.button_start_game

    def handle_event(self, event):
        """Override Scene.handle_event"""
        # xử lý sự kiện chuột
        if(event.type == pygame.MOUSEBUTTONDOWN):
            pass

        # xử lý sự kiện bàn phím
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RETURN):
                self.selected_button.handle_clicked()
            if(event.key == pygame.K_UP):
                self.__reset_button(self.button_exit)
                self.selected_button = self.button_start_game
            if(event.key == pygame.K_DOWN):
                self.__reset_button(self.button_start_game)
                self.selected_button = self.button_exit

    def update(self):
        """Override Scene.update"""
        self.selected_button.update()
        self.selected_button.draw(self._surface)

    # các method cụ thể để xử lý sự kiện của button cụ thể 
    def __handle_start_game_clicked(self):
        print("Start Game Clicked - scene.main_menu.handle_start_game_clicked")
        # Thực hiện logic khi nhấn nút start game bên dưới
        # Todo: Thay đổi current_scene của GameManger sang màn hình GamePlay
        # ...

    def __handle_exit_clicked(self):
        print("Exit Clicked - scene.main_menu.handle_exit_clicked")
        sys.exit()

    def __reset_button(self, button):
        button.reset()
        button.draw(self._surface)