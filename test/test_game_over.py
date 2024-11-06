import sys
import pygame
import src.utils.constant as const
from src.scenes.game_over import GameOver
from src.scenes.main_menu import MainMenu
from src.scenes.gameplay import GamePlay

class TestOverGame:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(True)
        pygame.display.set_caption('PacMan')

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT), pygame.FULLSCREEN)

        # Khởi tạo các màn hình
        self.scenes = {
            "GameOver": GameOver(self),
            "MainMenu": MainMenu(self),
            "GamePlay": GamePlay(self)  # Đảm bảo GamePlay tồn tại
        }
        self.current_scene = self.scenes["GameOver"]  # Bắt đầu với màn hình Game Over
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.render()

            pygame.display.flip()
            self.clock.tick(const.FPS)

        self.exit()

    def switch_scene(self, scene_name):
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.reset()  # Đặt lại trạng thái của cảnh mới


    def exit(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    TestOverGame().run()
