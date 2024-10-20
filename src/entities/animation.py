import src.entities as entities
from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader


class Animation:
    """Class giúp quản lý animation cho Pacman và Ghost"""

    def __init__(self, entity):
        self.entity = entity
        self.index = 0
        self.frame_tick = 0
        self.frame_rate = 5
        if isinstance(entity, entities.pacman.Pacman):
            self.sprites = self.SpriteSheets.pacman()

    def next(self):
        """ Lấy ra hình ảnh cho frame tiếp theo """
        self.index = (self.index + 1) % len(self.sprites[self.entity.get_direction()])
        return self.current()

    def current(self):
        """ Lấy ra hình ảnh của frame hiện tại """
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
        def ghost():
            # TODO: lấy sprite sheets của ghost
            pass
