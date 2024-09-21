from component.button import Button
from utils.constant import SCALE, WIDTH
from utils.spriteLoader import SpriteLoader

class ButtonFactory:
    @staticmethod
    def create_btn_start_game():
        topleft = ((WIDTH-80*SCALE)//2, 220)
        return Button("Start Game", "white", "red", topleft)
    
    @staticmethod
    def create_btn_exit():
        topleft = (((WIDTH-40*SCALE)//2, 270))
        return Button("Exit", "white", "red", topleft)
