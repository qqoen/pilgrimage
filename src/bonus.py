import pyray as rl
from src.game_object import GameObject
from src.sprite import Sprite
from src.asset_store import AssetStore
from src.constants import AREA_HEIGHT
from src.utils import play_sound


class Bonus(GameObject):
    def __init__(self, x, y, score):
        super().__init__(Sprite(AssetStore.get("bonus"), 3), 34)
        self.position.x = x
        self.position.y = y
        self.score = score
        self.speed = -10
        self.acceleration = 150
        self.is_destroyed = False
        self.frame_count = 0
        self.attract_radius = self.hit_radius * 3

    def is_near(self, other: GameObject):
        return rl.check_collision_circles(self.position, self.attract_radius, other.position, other.hit_radius)

    def update(self, dt):
        self.position.y += self.speed * dt

        if self.y >= AREA_HEIGHT:
            self.is_destroyed = True

        self.frame_count += 1
        self.speed += self.acceleration * dt

    def pick(self):
        play_sound(AssetStore.get("pickup"))
        self.is_destroyed = True
