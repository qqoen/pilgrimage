import pyray as rl
import random
from src.common import play_sound
from src.asset_store import AssetStore
from src.sprite import Sprite
from src.bonus import Bonus
from src.game_object import GameObject
from src.constants import WINDOW_HEIGHT
from src.data import EnemyType
from src.bullet_emitter import BulletEmitter


class Enemy(GameObject):
    def __init__(self, enemy: EnemyType, emitter: BulletEmitter):
        super().__init__(Sprite(AssetStore.get(enemy["texture"]), 3), 12)
        self.speed = enemy["speed"]
        self.health = enemy["health"]
        self.hit_frames = 0.0
        self.emitter = emitter

    @GameObject.x.setter
    def x(self, value):
        self.position.x = value
        self.emitter.position.x = value

    @GameObject.y.setter
    def y(self, value):
        self.position.y = value
        self.emitter.position.y = value

    def update(self, dt: float):
        self.y += self.speed * dt

        if self.hit_frames > 0:
            self.sprite.tint = rl.RED
            self.hit_frames -= 25 * dt
        else:
            self.sprite.tint = rl.WHITE
            self.hit_frames = 0

        if self.position.y >= WINDOW_HEIGHT:
            self.is_destroyed = True

        self.emitter.update(dt)

    def draw(self):
        super().draw()

    def hit(self):
        if self.y <= 0:
            return []

        self.health -= 1
        self.x += random.randint(-3, 3)
        bonuses = []

        if self.health <= 0:
            play_sound(AssetStore.get("destroy_sound"))
            self.is_destroyed = True
            bonuses.append(Bonus(self.x, self.y, 30))
        else:
            play_sound(AssetStore.get("hit_sound"))
            self.hit_frames = 1

        return bonuses

