import random
import pygame
from src.entities.Sprite import Sprite
from src.entities.animation import Animation
from src.utils.astar_pathfinding import AStarPathfinding
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction
import src.utils.debugger as debugger


class Ghost(Sprite):
    # MODE: Các trạng thái hoạt động của Ghost
    FRIGHTENED = 1  # Trạng thái sợ hãi
    CHASE = 2       # Trạng thái đuổi theo Pacman
    SCATTER = 3     # Trạng thái di chuyển về góc cố định
    DEAD = 4        # Trạng thái "chết", quay về điểm spawn

    def __init__(self, animation, hitbox, ai_strategy):
        self.ai_strategy = ai_strategy  # Chiến lược AI điều khiển Ghost
        self.mode = None  # Trạng thái ban đầu
        self.is_frightened_flash = False  # Biến để xác định trạng thái nhấp nháy khi gần hết FRIGHTENED
        self.last_time_switch_mode = 0  # Thời gian chuyển trạng thái gần nhất
        self.mode_duration = 0  # Thời gian duy trì trạng thái hiện tại
        super().__init__(animation, hitbox)

    def update(self):
        self._animation.update()  # Cập nhật animation
        if self.mode == Ghost.FRIGHTENED:
            self.update_frightened_animation()  # Cập nhật trạng thái nhấp nháy khi sợ hãi

    def execute_ai(self, maze):
        self.ai_strategy.execute(self, maze)  # Thực thi chiến lược AI

    def name(self):
        pass

    def switch_mode(self, mode, duration):
        # Chuyển trạng thái Ghost và đặt thời gian duy trì
        self.mode = mode
        self.last_time_switch_mode = pygame.time.get_ticks()
        self.mode_duration = duration

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
    def __init__(self):
        animation = Animation(self, 'ghost_red')  # Animation mặc định
        hitbox = pygame.Rect(0, 0, BLOCK_SIZE * SCALE, BLOCK_SIZE * SCALE)  # Kích thước hitbox
        super().__init__(animation, hitbox, RedAIStrategy())

    def name(self):
        return 'ghost_red'

# TODO: Tương tự GhostRed - thay đổi phương thức name "ghost_red", thay đổi chiến thuật AI "OrangeAIStrategy"
class GhostOrange(Ghost):
    pass

# TODO: Tương tự GhostCyan - thay đổi phương thức name "ghost_cyan", thay đổi chiến thuật AI "CyanAIStrategy"
class GhostCyan(Ghost):
    pass

# TODO: Tương tự GhostPink - thay đổi phương thức name "ghost_pink", thay đổi chiến thuật AI "PinkAIStrategy"
class GhostPink(Ghost):
    pass


### AI class
from abc import ABC, abstractmethod

""" Lớp cha (abstract) cho các chiến lược AI """
class BasicAIStrategy(ABC):
    def __init__(self):
        self.scatter_step = 0  # Bước hiện tại trong chế độ SCATTER
        self.algo = AStarPathfinding()  # Thuật toán tìm đường A*

    @abstractmethod
    def execute(self, ghost, maze):
        pass

    def move_to(self, ghost, dest):
        # Di chuyển Ghost đến đích
        path = self.algo.execute(ghost.get_position(), dest)
        if path is None:
            # Nếu không tìm thấy đường, chọn hướng ngẫu nhiên
            directs = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            random_choice = random.choice(directs)
            ghost.set_next_direction(random_choice)
        elif path and len(path) > 0:
            # Kiểm tra nếu Ghost đang ở trung tâm ô hiện tại
            hitbox_center = ghost.get_hitbox().center
            c, r = ghost.get_position()
            center_x = int(c * BLOCK_SIZE * SCALE + (BLOCK_SIZE * SCALE) // 2)
            center_y = int(r * BLOCK_SIZE * SCALE + (BLOCK_SIZE * SCALE) // 2)

            debugger.set_attributes('path', path)
            next = path[0].position  # Lấy bước tiếp theo
            dx = next[0] - ghost.get_position()[0]
            dy = next[1] - ghost.get_position()[1]

            # Chỉ thay đổi hướng khi Ghost ở trung tâm ô
            if hitbox_center[0] == center_x and hitbox_center[1] == center_y:
                if dx > 0:
                    ghost.set_next_direction(Direction.RIGHT)
                elif dx < 0:
                    ghost.set_next_direction(Direction.LEFT)
                elif dy > 0:
                    ghost.set_next_direction(Direction.DOWN)
                elif dy < 0:
                    ghost.set_next_direction(Direction.UP)

""" Chiến lược riêng cho GhostRed """
class RedAIStrategy(BasicAIStrategy):
    # Chiến lược AI cho Ghost đỏ
    SPAWN_ROW_COL = (14, 15)  # Vị trí spawn ban đầu theo row, col trong grid
    SPAWN_POS = (SPAWN_ROW_COL[1], SPAWN_ROW_COL[0]) # Vị trí theo x,y
    SCATTER_POS = [(1, 1), (6, 5)]  # Các điểm đến trong chế độ SCATTER
    SCATTER_DURATION = 10  # Thời gian SCATTER
    CHASE_DURATION = 20  # Thời gian CHASE
    WAITING_DURATION = 3  # Thời gian chờ trước khi bắt đầu

    def execute(self, ghost, maze):
        # Tự động chuyển đổi trạng thái dựa trên thời gian
        self.auto_switch_mode(ghost)

        # Xác định đích đến dựa trên trạng thái hiện tại
        if ghost.mode == Ghost.CHASE:
            dest = maze.get_pacman_pos()  # Đuổi theo Pacman
            ghost._speed = 2
        elif ghost.mode == Ghost.FRIGHTENED:
            dest = self.SPAWN_POS  # Chạy về vị trí spawn
            ghost._speed = 1
        elif ghost.mode == Ghost.SCATTER:
            ghost._speed = 2
            dest = self.SCATTER_POS[self.scatter_step]
            if ghost.get_position() == dest:
                # Chuyển sang điểm SCATTER tiếp theo
                self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        elif ghost.mode == Ghost.DEAD:
            ghost._speed = 5
            dest = self.SPAWN_POS  # Quay về điểm spawn khi chết
        else:
            dest = self.SPAWN_POS
            ghost._speed = 1

        self.move_to(ghost, dest)

    def auto_switch_mode(self, ghost):
        # Tự động chuyển trạng thái dựa trên thời gian
        if ghost.mode == Ghost.FRIGHTENED:
            return
        if ghost.mode == Ghost.DEAD and ghost.get_position() == self.SPAWN_POS:
            ghost.mode_duration = 0
            ghost.mode = None
            return

        if ghost.last_time_switch_mode == 0:
            ghost.last_time_switch_mode = pygame.time.get_ticks()

        delta_time = (pygame.time.get_ticks() - ghost.last_time_switch_mode) // 1000

        if delta_time > self.WAITING_DURATION and ghost.mode is None:
            ghost.switch_mode(Ghost.SCATTER, self.SCATTER_DURATION)
        elif delta_time > self.SCATTER_DURATION and ghost.mode != Ghost.CHASE:
            ghost.switch_mode(Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.CHASE_DURATION and ghost.mode != Ghost.SCATTER:
            ghost.switch_mode(Ghost.SCATTER, self.SCATTER_DURATION)

# TODO: Có thể tương tự RedAIStrategy - thay đổi các chiến lược như: thời gian, vị trí di chuyển ...
class OrangeAIStrategy(BasicAIStrategy):

    def execute(self, ghost, maze):
        """ Hàm kế thừa từ lớp BasicAIStrategy để thực thi thuật toán"""
        pass

# TODO: Có thể tương tự RedAIStrategy - thay đổi các chiến lược như: thời gian, vị trí di chuyển ...
class PinkAIStrategy(BasicAIStrategy):

    def execute(self, ghost, maze):
        """ Hàm kế thừa từ lớp BasicAIStrategy để thực thi thuật toán"""
        pass

# TODO: Có thể tương tự RedAIStrategy - thay đổi các chiến lược như: thời gian, vị trí di chuyển ...
class CyanAIStrategy(BasicAIStrategy):

    def execute(self, ghost, maze):
        """ Hàm kế thừa từ lớp BasicAIStrategy để thực thi thuật toán"""
        pass
