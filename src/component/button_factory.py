from component.button import Button
from utils.spriteLoader import SpriteLoader

class ButtonFactory:
    @staticmethod
    def create_btn_start_game(topleft):
        default_img = SpriteLoader().text_start_game_white()
        hovered_img = SpriteLoader().text_start_game_cyan()
        return Button(default_img, hovered_img, topleft)
    
    @staticmethod
    def create_btn_exit(topleft):
        default_img = SpriteLoader().text_exit_white()
        hovered_img = SpriteLoader().text_exit_cyan()
        return Button(default_img, hovered_img, topleft)
