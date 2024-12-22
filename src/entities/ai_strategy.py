import random
import pygame

import src.utils.debugger as debugger
import src.entities.ghost as g
from src.utils.constant import BLOCK_SIZE, SCALE
from src.utils.enum import Direction
from src.utils.astar_pathfinding import AStarPathfinding
from abc import ABC, abstractmethod

""" Lớp cha (abstract) cho các chiến lược AI """
class BasicAIStrategy(ABC):
    def __init__(self):
        self.last_pos = None
        self.scatter_step = 0  # Bước hiện tại trong chế độ SCATTER
        self.algo = AStarPathfinding()  # Thuật toán tìm đường A*

    @abstractmethod
    def execute(self, ghost, maze):
        pass

    def move_to(self, ghost, dest):
        # Di chuyển Ghost đến đích
        path = self.algo.execute(ghost.get_position(), dest)  # Truyền maze cho thuật toán A*
        if path is None: return self.last_pos
            # # Nếu không tìm thấy đường, chọn hướng ngẫu nhiên
            # directs = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            # random_choice = random.choice(directs)
            # ghost.set_next_direction(random_choice)
            # self.last_direction = random_choice  # Cập nhật hướng cuối cùng
        elif path and len(path) > 0:
            # Kiểm tra nếu Ghost đang ở trung tâm ô hiện tại
            hitbox_center = ghost.get_hitbox().center
            c, r = ghost.get_position()
            center_x = int(c * BLOCK_SIZE * SCALE + (BLOCK_SIZE * SCALE) // 2)
            center_y = int(r * BLOCK_SIZE * SCALE + (BLOCK_SIZE * SCALE) // 2)

            if ghost.name() in debugger.ghost_paths:
                debugger.set_attributes(debugger.ghost_paths[ghost.name()], path)

            next = path[0].position  # Lấy bước tiếp theo
            self.last_pos = next
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


""" AI Strategy cho GhostRed """
class RedAIStrategy(BasicAIStrategy):
    # Chiến lược AI cho Ghost đỏ
    SPEED = 2
    CENTER_POS = (14, 14)
    SPAWN_ROW_COL = (14, 18)  # Vị trí spawn ban đầu theo row, col trong grid
    HOME_POS = (SPAWN_ROW_COL[1], SPAWN_ROW_COL[0])  # Vị trí theo x,y
    SCATTER_POS = [(1, 1), (6, 5)]  # Các điểm đến trong chế độ SCATTER
    SCATTER_DURATION = 10  # Thời gian SCATTER
    CHASE_DURATION = 20  # Thời gian CHASE
    WAITING_DURATION = -1  # Thời gian chờ trước khi bắt đầu

    def execute(self, ghost, maze):
        # Tự động chuyển đổi trạng thái dựa trên thời gian
        self.auto_switch_mode(ghost)

        # Xác định đích đến dựa trên trạng thái hiện tại
        dest = maze.get_pacman_pos()
        if ghost.mode == g.Ghost.CHASE:
            dest = maze.get_pacman_pos()  # Đuổi theo Pacman
            ghost._speed = self.SPEED
        elif ghost.mode == g.Ghost.FRIGHTENED:
            dest = self.HOME_POS  # Chạy về vị trí trung tâm
            ghost._speed = max(1, self.SPEED-1)
        elif ghost.mode == g.Ghost.SCATTER:
            ghost._speed = self.SPEED
            dest = self.SCATTER_POS[self.scatter_step]
            if ghost.get_position() == dest:
                # Chuyển sang điểm SCATTER tiếp theo
                self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        elif ghost.mode == g.Ghost.DEAD:
            ghost._speed = 5 # fix cứng 5 (ko thay đổi qua các level)
            dest = self.HOME_POS  # Quay về điểm spawn khi chết
        else:
            dest = self.HOME_POS
            ghost._speed = 1 # fix cứng 1 (ko thay đổi qua các level)

        self.move_to(ghost, dest)

    def auto_switch_mode(self, ghost):
        # Tự động chuyển trạng thái dựa trên thời gian
        if ghost.mode == g.Ghost.FRIGHTENED:
            return
        if ghost.mode == g.Ghost.DEAD and ghost.get_position() == self.HOME_POS:
            ghost.mode_duration = 0
            ghost.mode = None
            return

        if ghost.last_time_switch_mode == 0:
            ghost.last_time_switch_mode = pygame.time.get_ticks()

        delta_time = (pygame.time.get_ticks() - ghost.last_time_switch_mode) // 1000

        if delta_time > self.WAITING_DURATION and ghost.mode is None:
            ghost.switch_mode(g.Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.SCATTER_DURATION and ghost.mode != g.Ghost.CHASE:
            ghost.switch_mode(g.Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.CHASE_DURATION and ghost.mode != g.Ghost.SCATTER:
            ghost.switch_mode(g.Ghost.SCATTER, self.SCATTER_DURATION)


""" AI Strategy cho GhostOrange """
class OrangeAIStrategy(BasicAIStrategy):
    SPEED = 2
    CENTER_POS = (14, 14)
    SPAWN_ROW_COL = (14, 9)
    HOME_POS = (SPAWN_ROW_COL[1], SPAWN_ROW_COL[0])  # x, y
    SCATTER_POS = [(1, 29), (12, 29), (6, 26)] #x, y
    SCATTER_DURATION = 10
    CHASE_DURATION = 20
    WAITING_DURATION = -1

    def __init__(self):
        # Khởi tạo đúng các thuộc tính của lớp cha
        super().__init__()  # Gọi __init__ của lớp BasicAIStrategy
        self.last_random_pos_time = pygame.time.get_ticks()  # Không cần thiết nữa
        self.random_position = (0, 0)  # Vị trí mặc định ban đầu
        self.target_corner = None

    def execute(self, ghost, maze):
        """Thực thi thuật toán AI của Orange"""
        self.auto_switch_mode(ghost)

        if ghost.mode == g.Ghost.CHASE:
            pacman_pos = maze.get_pacman_pos()
            ghost_pos = ghost.get_position()
            dest = self.calculate_target_position(pacman_pos, ghost_pos)
            ghost._speed = self.SPEED
        elif ghost.mode == g.Ghost.FRIGHTENED:
            dest = self.HOME_POS
            ghost._speed = max(1, self.SPEED-1)
        elif ghost.mode == g.Ghost.SCATTER:
            dest = self.SCATTER_POS[self.scatter_step]
            ghost._speed = self.SPEED
            if ghost.get_position() == dest:
                # Chuyển sang điểm SCATTER tiếp theo
                self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        elif ghost.mode == g.Ghost.DEAD:
            dest = self.HOME_POS
            ghost._speed = 5
        else:
            dest = self.HOME_POS
            ghost._speed = 1

        self.move_to(ghost, dest)

    def auto_switch_mode(self, ghost):
        """Chuyển đổi giữa các chế độ hoạt động tự động"""
        if ghost.mode == g.Ghost.FRIGHTENED:
            return
        if ghost.mode == g.Ghost.DEAD and ghost.get_position() == self.HOME_POS:
            ghost.mode_duration = 0
            ghost.mode = None
            ghost.set_speed_based_on_level()  # Cập nhật tốc độ
            return

        if ghost.last_time_switch_mode == 0:
            ghost.last_time_switch_mode = pygame.time.get_ticks()

        delta_time = (pygame.time.get_ticks() - ghost.last_time_switch_mode) // 1000

        if delta_time > self.WAITING_DURATION and ghost.mode is None:
            ghost.switch_mode(g.Ghost.SCATTER, self.SCATTER_DURATION)
        elif delta_time > self.SCATTER_DURATION and ghost.mode != g.Ghost.CHASE:
            ghost.switch_mode(g.Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.CHASE_DURATION and ghost.mode != g.Ghost.SCATTER:
            ghost.switch_mode(g.Ghost.SCATTER, self.SCATTER_DURATION)

    def calculate_distance(self, pos1, pos2):
        """Tính khoảng cách giữa hai điểm"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def calculate_target_position(self, pacman_pos, ghost_pos):
        distance = self.calculate_distance(pacman_pos, ghost_pos)
        dest = self.target_corner
        if distance > 8:
            if self.target_corner is None:
                dest = pacman_pos
            elif distance > 12:
                self.target_corner = None
        elif distance <= 8:
            if self.target_corner is None:
                # Các góc có thể chọn
                corners = [(1, 1), (1, 29), (26, 1), (26, 29)]
                self.target_corner = random.choice(corners)
                dest = self.target_corner
        return dest


""" AI Strategy cho PinkGhost """
class PinkAIStrategy(BasicAIStrategy):
    SPAWN_ROW_COL = (14, 15) #(row, col)
    HOME_POS = (SPAWN_ROW_COL[1], SPAWN_ROW_COL[0])  # (x, y)
    SCATTER_POS = [(26,29), (15, 29), (20, 23)] # (x, y)
    SCATTER_DURATION = 10
    CHASE_DURATION = 15
    WAITING_DURATION = 3
    ghost_pos = None
    def execute(self, ghost, maze):
        """
        Thực hiện thuật toán AI cho Ghost Pink.
        Mục tiêu: Theo đuổi một vị trí cách Pacman 3 ô theo hướng di chuyển hiện tại của Pacman.
        """
        self.auto_switch_mode(ghost)
        pacman_pos = maze.get_pacman_pos()
        pacman_dir = maze.get_pacman_direction()
        self.ghost_pos = ghost.get_position()

        dest = ghost.get_position()
        if ghost.mode == g.Ghost.CHASE:
            dest = self.calculate_target_position(pacman_pos, pacman_dir)
            ghost._speed = 2
        elif ghost.mode == g.Ghost.FRIGHTENED:
            dest = self.HOME_POS
            ghost._speed = 1
        elif ghost.mode == g.Ghost.SCATTER:
            ghost._speed = 2
            dest = self.SCATTER_POS[self.scatter_step]
            if ghost.get_position() == dest: self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        elif ghost.mode == g.Ghost.DEAD:
            dest = self.HOME_POS
            ghost._speed = 5
        else:
            dest = self.HOME_POS
            ghost._speed = 1

        self.move_to(ghost, dest)

    def auto_switch_mode(self, ghost):
        """Chuyển đổi giữa các chế độ hoạt động tự động"""
        if ghost.mode == g.Ghost.FRIGHTENED:
            return
        if ghost.mode == g.Ghost.DEAD and ghost.get_position() == self.HOME_POS:
            ghost.mode_duration = 0
            ghost.mode = None
            ghost.set_speed_based_on_level()  # Cập nhật tốc độ
            return

        if ghost.last_time_switch_mode == 0:
            ghost.last_time_switch_mode = pygame.time.get_ticks()

        delta_time = (pygame.time.get_ticks() - ghost.last_time_switch_mode) // 1000

        if delta_time > self.WAITING_DURATION and ghost.mode is None:
            ghost.switch_mode(g.Ghost.SCATTER, self.SCATTER_DURATION)
        elif delta_time > self.SCATTER_DURATION and ghost.mode != g.Ghost.CHASE:
            ghost.switch_mode(g.Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.CHASE_DURATION and ghost.mode != g.Ghost.SCATTER:
            ghost.switch_mode(g.Ghost.SCATTER, self.SCATTER_DURATION)

    def calculate_target_position(self, pacman_pos, pacman_dir):
        """
        Tính toán vị trí mục tiêu cách Pacman 3 ô theo hướng di chuyển hiện tại.

        :param pacman_pos: Vị trí hiện tại của Pacman (x, y).
        :param pacman_dir: Hướng di chuyển hiện tại của Pacman (Direction).
        :return: Vị trí mục tiêu (x, y).
        """
        x, y = pacman_pos
        target_pos = (x, y)
        if pacman_dir == Direction.UP:
            target_pos = (x, y - 3)
        elif pacman_dir == Direction.DOWN:
            target_pos = (x, y + 3)
        elif pacman_dir == Direction.LEFT:
            target_pos = (x - 3, y)
        elif pacman_dir == Direction.RIGHT:
            target_pos = (x + 3, y)

        return target_pos


""" AI Strategy cho CyanGhost """
class CyanAIStrategy(BasicAIStrategy):
    SPAWN_ROW_COL = (14, 12)  # Vị trí spawn
    HOME_POS = (SPAWN_ROW_COL[1], SPAWN_ROW_COL[0])
    SCATTER_POS = [(26, 1), (21, 5)]  # Góc dưới bên phải
    SCATTER_DURATION = 10
    CHASE_DURATION = 20
    WAITING_DURATION = 3

    def execute(self, ghost, maze):
        self.auto_switch_mode(ghost)

        dest = ghost.get_position()
        if ghost.mode == g.Ghost.CHASE:
            dest = self.calculate_target_position(maze)
            ghost._speed = 2
        elif ghost.mode == g.Ghost.FRIGHTENED:
            dest = self.HOME_POS
            ghost._speed = 1
        elif ghost.mode == g.Ghost.SCATTER:
            ghost._speed = 2
            dest = self.SCATTER_POS[self.scatter_step]
            if ghost.get_position() == dest: self.scatter_step = (self.scatter_step + 1) % len(self.SCATTER_POS)
        elif ghost.mode == g.Ghost.DEAD:
            dest = self.HOME_POS
            ghost._speed = 5
        else:
            dest = self.HOME_POS
            ghost._speed = 1

        self.move_to(ghost, dest)

    def auto_switch_mode(self, ghost):
        """Chuyển đổi giữa các chế độ hoạt động tự động"""
        if ghost.mode == g.Ghost.FRIGHTENED:
            return
        if ghost.mode == g.Ghost.DEAD and ghost.get_position() == self.HOME_POS:
            ghost.mode_duration = 0
            ghost.mode = None
            ghost.set_speed_based_on_level()  # Cập nhật tốc độ
            return

        if ghost.last_time_switch_mode == 0:
            ghost.last_time_switch_mode = pygame.time.get_ticks()

        delta_time = (pygame.time.get_ticks() - ghost.last_time_switch_mode) // 1000

        if delta_time > self.WAITING_DURATION and ghost.mode is None:
            ghost.switch_mode(g.Ghost.SCATTER, self.SCATTER_DURATION)
        elif delta_time > self.SCATTER_DURATION and ghost.mode != g.Ghost.CHASE:
            ghost.switch_mode(g.Ghost.CHASE, self.CHASE_DURATION)
        elif delta_time > self.CHASE_DURATION and ghost.mode != g.Ghost.SCATTER:
            ghost.switch_mode(g.Ghost.SCATTER, self.SCATTER_DURATION)

    def calculate_target_position(self, maze):
        """Tính toán vị trí mục tiêu của Inky."""
        pacman_pos = maze.get_pacman_pos()
        pacman_dir = maze.get_pacman_direction()

        # Tìm Blinky (ghost đỏ)
        blinky = None
        for ghost in maze.get_ghosts():
            if isinstance(ghost, g.GhostRed):
                blinky = ghost
                break

        if blinky is None:
            return pacman_pos  # Nếu không tìm thấy Blinky, đuổi theo Pacman

        # # Vị trí 2 ô phía trước Pacman
        # if pacman_dir == Direction.UP:
        #     target_temp = (pacman_pos[0], pacman_pos[1] - 2)
        # elif pacman_dir == Direction.DOWN:
        #     target_temp = (pacman_pos[0], pacman_pos[1] + 2)
        # elif pacman_dir == Direction.LEFT:
        #     target_temp = (pacman_pos[0] - 2, pacman_pos[1])
        # elif pacman_dir == Direction.RIGHT:
        #     target_temp = (pacman_pos[0] + 2, pacman_pos[1])
        # else:
        #     target_temp = pacman_pos  # Trường hợp không có hướng
        #
        # # Vector từ Blinky đến vị trí tạm tính
        # vector_x = target_temp[0] - blinky.get_position()[0]
        # vector_y = target_temp[1] - blinky.get_position()[1]
        #
        # # Nhân đôi vector và cộng vào vị trí Blinky để có mục tiêu cuối cùng
        # target_x = blinky.get_position()[0] + (2 * vector_x)
        # target_y = blinky.get_position()[1] + (2 * vector_y)

        return blinky.get_position()[0], maze.get_pacman_pos()[1]


#----------------------------------
# AI STRATEGY CHO LEVEL 1
#----------------------------------
class RedAIStrategyLv1(RedAIStrategy):
    SPEED = 2
    SPAWN_ROW_COL = (14, 15) #(row, col)
    HOME_POS = (15, 14)  # Vị trí theo x,y
    SCATTER_DURATION = 15  # Thời gian SCATTER
    CHASE_DURATION = 15  # Thời gian CHASE
    WAITING_DURATION = 3  # Thời gian chờ trước khi bắt đầu

class OrangeAIStrategyLv1(OrangeAIStrategy):
    SPEED = 2
    SPAWN_ROW_COL = (14, 12)  # Vị trí spawn
    HOME_POS = (12, 14)
    SCATTER_DURATION = 10
    CHASE_DURATION = 10
    WAITING_DURATION = 5


#----------------------------------
# AI STRATEGY CHO LEVEL 2
#----------------------------------
class RedAIStrategyLv2(RedAIStrategy): pass

class OrangeAIStrategyLv2(OrangeAIStrategy): pass

class PinkAIStrategyLv2(PinkAIStrategy): pass

class CyanAIStrategyLv2(CyanAIStrategy): pass


#----------------------------------
# AI STRATEGY CHO LEVEL 3
#----------------------------------
class RedAIStrategyLv3(RedAIStrategy): pass

class OrangeAIStrategyLv3(OrangeAIStrategy): pass

class PinkAIStrategyLv3(PinkAIStrategy): pass

class CyanAIStrategyLv3(CyanAIStrategy): pass