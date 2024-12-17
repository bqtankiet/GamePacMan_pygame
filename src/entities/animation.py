from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader


class Animation:
    """Class giúp quản lý animation cho Pacman và Ghost"""

    def __init__(self, entity, sprite_name, frame_rate = 5):
        self.entity = entity
        self.index = 0
        self.frame_tick = 0
        self.frame_rate = frame_rate
        self.sprite_name = sprite_name.lower()
        if   self.sprite_name == "pacman": self.sprites = self.SpriteSheets.pacman()
        elif self.sprite_name == "ghost_red": self.sprites = self.SpriteSheets.ghost('red')
        elif self.sprite_name == "ghost_pink": self.sprites = self.SpriteSheets.ghost('pink')
        elif self.sprite_name == "ghost_orange": self.sprites = self.SpriteSheets.ghost('orange')
        elif self.sprite_name == "ghost_cyan": self.sprites = self.SpriteSheets.ghost('cyan')
        elif self.sprite_name == "frightened": self.sprites = self.SpriteSheets.frightened()
        elif self.sprite_name == "frightened_flash": self.sprites = self.SpriteSheets.frightened_flash()
        elif self.sprite_name == "ghost_dead": self.sprites = self.SpriteSheets.ghost_dead()
        elif self.sprite_name == "pacman_dead": self.sprites = self.SpriteSheets.pacman_dead()

    def next(self):
        """ Lấy ra hình ảnh cho frame tiếp theo """
        if self.sprite_name == "pacman_dead":
            self.index = min(self.index + 1, 11)
        else:
            self.index = (self.index + 1) % len(self.sprites[self.entity.get_direction()])
        return self.current()

    def current(self):
        """ Lấy ra hình ảnh của frame hiện tại """
        if self.sprite_name == "pacman_dead":
            return self.sprites[self.index]
        else:
            return self.sprites[self.entity.get_direction()][self.index]

    def update(self):
        """ Cập nhật hình ảnh của thực thể """
        self.frame_tick += 1
        if self.frame_tick >= self.frame_rate:
            self.frame_tick = 0
            self.entity.image = self.next()
        else:
            self.entity.image = self.current()

    class SpriteSheets:
        """Inner Class để lấy các sprite sheets của Pacman hoặc Ghost"""

        @staticmethod
        def pacman():
            img = ImageLoader()
            return {
                Direction.LEFT: (img.pacman_0(), img.pacman_l1(), img.pacman_l2(), img.pacman_l1()),
                Direction.RIGHT: (img.pacman_0(), img.pacman_r1(), img.pacman_r2(), img.pacman_r1()),
                Direction.UP: (img.pacman_0(), img.pacman_u1(), img.pacman_u2(), img.pacman_u1()),
                Direction.DOWN: (img.pacman_0(), img.pacman_d1(), img.pacman_d2(), img.pacman_d1())
            }

        @staticmethod
        def ghost(color):
            img = ImageLoader()
            return {
                Direction.LEFT: (img.ghost(color, 'l1'), img.ghost(color, 'l2')),
                Direction.RIGHT: (img.ghost(color, 'r1'), img.ghost(color, 'r2')),
                Direction.UP: (img.ghost(color, 'u1'), img.ghost(color, 'u2')),
                Direction.DOWN: (img.ghost(color, 'd1'), img.ghost(color, 'd2')),
            }

        @staticmethod
        def frightened():
            img = ImageLoader()
            tmp = (img.frightened_1(), img.frightened_2())
            return {
                Direction.LEFT: tmp,
                Direction.RIGHT: tmp,
                Direction.UP: tmp,
                Direction.DOWN: tmp,
            }

        @staticmethod
        def frightened_flash():
            img = ImageLoader()
            tmp = (img.frightened_1(),  img.frightened_2('white'), img.frightened_1('white'), img.frightened_2())
            return {
                Direction.LEFT: tmp,
                Direction.RIGHT: tmp,
                Direction.UP: tmp,
                Direction.DOWN: tmp,
            }

        @staticmethod
        def ghost_dead():
            img = ImageLoader()
            return {
                Direction.LEFT: (img.ghost_dead('left'),img.ghost_dead('left')),
                Direction.RIGHT: (img.ghost_dead('right'),img.ghost_dead('right')),
                Direction.UP: (img.ghost_dead('up'),img.ghost_dead('up')),
                Direction.DOWN: (img.ghost_dead('down'),img.ghost_dead('down')),
            }

        @staticmethod
        def pacman_dead():
            img = ImageLoader()
            sprites = []
            for i in range(12):
                sprites.append(img.pacman_dead(i))
            return sprites