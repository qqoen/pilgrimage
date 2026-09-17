import pyray as rl
from src.game_object import GameObject
from src.sprite import Sprite
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class Bullet(GameObject):
    def __init__(self, sprite: Sprite, direction: rl.Vector2, speed: float, radius: int):
        super().__init__(sprite, radius)
        self.direction = direction
        self.speed = speed

    def update(self, dt):
        self.position.x += self.direction.x * self.speed * dt
        self.position.y += self.direction.y * self.speed * dt

        if self.position.x <= -self.width() or self.position.x >= WINDOW_WIDTH + self.width()\
            or self.position.y <= -self.height() or self.position.y >= WINDOW_HEIGHT + self.height():
            self.is_destroyed = True
