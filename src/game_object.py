import pyray as rl
from src.sprite import Sprite
from src.constants import IS_DEBUG


class GameObject:
    def __init__(self, sprite: Sprite, hit_radius: int):
        self.sprite = sprite
        self.position = rl.Vector2(0, 0)
        self.hit_radius = hit_radius
        self.is_destroyed = False

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def width(self):
        return self.sprite.width

    @property
    def height(self):
        return self.sprite.height

    @property
    def center(self):
        return rl.vector2_add(self.position, (self.width // 2, self.height // 2))

    def is_hit(self, other: GameObject):
        return rl.check_collision_circles(self.position, self.hit_radius, other.position, other.hit_radius)

    def draw(self):
        self.sprite.draw(self.position.x, self.position.y)

        if IS_DEBUG:
            # rl.draw_circle_v(self.position, self.hit_radius, rl.GREEN)
            pass
