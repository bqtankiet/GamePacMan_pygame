import src.entities as entities
from src.utils.enum import Direction
from src.utils.image_loader import ImageLoader

class Animation:
    """A class to manage animations for game entities such as Pacman and Ghost"""
    def __init__(self, entity):
        self.entity = entity
        self.index = 0
        self.frame_tick = 0
        self.frame_rate = 5
        if isinstance(entity, entities.pacman.Pacman):
            self.sprites = self.SpriteSheets.pacman()

    def next(self):
        """ get next sprite from current state """
        self.index = (self.index + 1) % len(self.sprites[self.entity.direction])
        return self.current()

    def current(self):
        """ get current sprite from current state """
        return self.sprites[self.entity.direction][self.index]

    def update(self):
        """ update entity's image """
        self.frame_tick += 1
        if self.frame_tick >= self.frame_rate:
            self.frame_tick = 0
            self.entity.image = self.next()
        else: self.entity.image = self.current()

    class SpriteSheets:
        """Animation inner class use to get image for animation"""
        @staticmethod
        def pacman():
            img = ImageLoader()
            return {
                Direction.LEFT: (img.pacman_0(), img.pacman_l1(), img.pacman_l2(), img.pacman_l1()),
                Direction.RIGHT: (img.pacman_0(), img.pacman_r1(), img.pacman_r2(), img.pacman_r1()),
                Direction.UP: (img.pacman_0(), img.pacman_u1(), img.pacman_u2(), img.pacman_u1()),
                Direction.DOWN: (img.pacman_0(), img.pacman_d1(), img.pacman_d2(), img.pacman_d1())
            }