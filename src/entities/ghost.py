from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.utils.constant import BLOCK_SIZE, SCALE
import src.core.game as game
import pygame
import src.entities.ai_strategy as ai

class Ghost(Sprite):
    """ Class cha của các class Ghost cụ thể """

    # MODE: Các trạng thái hoạt động của Ghost
    FRIGHTENED = 1  # Trạng thái sợ hãi
    CHASE = 2  # Trạng thái đuổi theo Pacman
    SCATTER = 3  # Trạng thái di chuyển về góc cố định
    DEAD = 4  # Trạng thái "chết", quay về điểm spawn

    def __init__(self, animation, hitbox, ai_strategy, level = 1):
        self.ai_strategy = ai_strategy  # Chiến lược AI điều khiển Ghost
        self.mode = None  # Trạng thái ban đầu
        self.is_frightened_flash = False  # Biến để xác định trạng thái nhấp nháy khi gần hết FRIGHTENED
        self.last_time_switch_mode = 0  # Thời gian chuyển trạng thái gần nhất
        self.mode_duration = 0  # Thời gian duy trì trạng thái hiện tại
        self.level = level

        super().__init__(animation, hitbox)

    def update(self):
        self._animation.update()
        self.set_speed_based_on_level()  # Cập nhật tốc độ ở mọi trạng thái
        if self.mode == Ghost.FRIGHTENED:
            self.update_frightened_animation()

    def execute_ai(self, maze):
        self.ai_strategy.execute(self, maze)  # Thực thi chiến lược AI

#-----------------------------------------------------------
    #Tang Toc Do Ghost Qua Cac Level
    def set_speed_based_on_level(self):
        self.level = game.Game.get_instance().game_status.level
        print('level', self.level)
        # if self.mode == Ghost.FRIGHTENED:
        #     self._speed = 1
        # elif self.mode == Ghost.CHASE:
        #     self._speed = Ghost.CHASE + int((self.level - 1) * 1)
        # elif self.mode == Ghost.SCATTER:
        #     self._speed = Ghost.SCATTER + int((self.level - 1) * 0.5)
        # elif self.mode == Ghost.DEAD:
        #     self._speed = 4
        # else:
        #     self._speed = 1
#------------------------------------------------------------
    def name(self):
        pass

    def switch_mode(self, mode, duration):
        # Chuyển trạng thái Ghost và đặt thời gian duy trì
        self.mode = mode
        self.last_time_switch_mode = pygame.time.get_ticks()
        self.mode_duration = duration

        # Cập nhật tốc độ mỗi khi chuyển trạng thái
        self.set_speed_based_on_level()

        # Cập nhật animation tương ứng với trạng thái
        if mode == Ghost.FRIGHTENED:
            self._animation = Animation(self, 'frightened')
        elif mode == Ghost.DEAD:
            self._animation = Animation(self, 'ghost_dead')
        else:
            self._animation = Animation(self, self.name())

    def update_frightened_animation(self):
        # Xử lý animation nhấp nháy khi gần hết thời gian FRIGHTENED
        duration = (pygame.time.get_ticks() - self.last_time_switch_mode) // 1000
        if duration > self.mode_duration - 2 and not self.is_frightened_flash:
            self._animation = Animation(self, 'frightened_flash')
            self.is_frightened_flash = True
        if duration > self.mode_duration:
            # Hết thời gian FRIGHTENED, chuyển về CHASE
            self.is_frightened_flash = False
            self.switch_mode(Ghost.CHASE, 10)


class GhostRed(Ghost):
    # Ghost màu đỏ, sử dụng chiến lược AI riêng
    def __init__(self, ai_strategy = ai.RedAIStrategy()):
        animation = Animation(self, 'ghost_red')  # Animation mặc định
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)  # Kích thước hitbox
        self.mode = Ghost.CHASE
        super().__init__(animation, hitbox, ai_strategy)

    def name(self):
        return 'ghost_red'


class GhostOrange(Ghost):
    # Ghost màu cam, sử dụng chiến lược AI riêng
    def __init__(self, ai_strategy = ai.OrangeAIStrategy()):
        animation = Animation(self, 'ghost_orange')  # Animation mặc định
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)  # Kích thước hitbox
        super().__init__(animation, hitbox, ai_strategy)

    def name(self):
        return 'ghost_orange'


class GhostCyan(Ghost):
    def __init__(self, ai_strategy = ai.CyanAIStrategy()):
        animation = Animation(self, 'ghost_cyan')
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)
        super().__init__(animation, hitbox, ai_strategy)

    def name(self):
        return 'ghost_cyan'


class GhostPink(Ghost):
    def __init__(self, ai_strategy = ai.PinkAIStrategy()):
        animation = Animation(self, 'ghost_pink')  # Animation mặc định
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)  # Kích thước hitbox
        self.mode = Ghost.SCATTER
        super().__init__(animation, hitbox, ai_strategy)

    def name(self):
        return 'ghost_pink'

