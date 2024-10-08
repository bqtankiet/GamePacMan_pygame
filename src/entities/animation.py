import src.entities as entities
from src.utils.image_loader import ImageLoader

class Animation:
    def __init__(self, entity):
        img = ImageLoader()
        self.entity = entity
        self.index = 0
        self.frame_tick = 0
        self.frame_rate = 5
        if isinstance(entity, entities.pacman.Pacman):
            self.sprites = self.SpritesFactory.pacman()

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

    class SpritesFactory:
        @staticmethod
        def pacman():
            img = ImageLoader()
            return {
                "left": (img.pacman_0(), img.pacman_l1(), img.pacman_l2(), img.pacman_l1()),
                "right": (img.pacman_0(), img.pacman_r1(), img.pacman_r2(), img.pacman_r1()),
                "up": (img.pacman_0(), img.pacman_u1(), img.pacman_u2(), img.pacman_u1()),
                "down": (img.pacman_0(), img.pacman_d1(), img.pacman_d2(), img.pacman_d1())
            }