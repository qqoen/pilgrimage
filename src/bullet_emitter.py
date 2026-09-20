import pyray as rl
import random
import math
from abc import ABC, abstractmethod
from src.bullet import Bullet
from src.sprite import Sprite
from src.asset_store import AssetStore
from src.utils import play_sound
from typing import Callable


BULLET_RADIUS = 6


class BulletEmitter(ABC):
    def __init__(self, bullets: list[Bullet], texture: str, emit_cooldown: float):
        self.bullets = bullets
        self.position = rl.Vector2()
        self.texture = texture
        self.emit_cooldown = emit_cooldown
        self.emit_timer: float = 0

    def move(self, x, y):
        self.position.x = x
        self.position.y = y

    def update(self, dt: float):
        if self.emit_timer <= 0:
            self.emit()
            self.emit_timer = self.emit_cooldown

        self.emit_timer -= dt

    def create_bullet(self, direction: rl.Vector2, speed: float):
        return Bullet(Sprite(AssetStore.get(self.texture), 3), rl.vector2_normalize(direction), speed, BULLET_RADIUS)

    @abstractmethod
    def emit(self, **kwargs):
        play_sound(AssetStore.get("enemy_shot"))


class EmptyEmitter(BulletEmitter):
    def __init__(self):
        super().__init__([], "", 0)

    def emit(self, **kwargs):
        pass


class SingleEmitter(BulletEmitter):
    def __init__(self, bullets, texture, cooldown, bullet_speed):
        super().__init__(bullets, texture, cooldown)
        self.bullet_speed = bullet_speed

    def emit(self, **kwargs):
        super().emit(**kwargs)
        bullet = self.create_bullet(rl.Vector2(0, 1), self.bullet_speed)
        bullet.position.x = self.position.x
        bullet.position.y = self.position.y
        self.bullets.append(bullet)


class SingleAimedEmitter(BulletEmitter):
    def __init__(self, bullets, texture, cooldown, get_player_position: Callable):
        super().__init__(bullets, texture, cooldown)
        self.get_player_position = get_player_position

    def emit(self, **kwargs):
        super().emit(**kwargs)
        player_position = self.get_player_position()
        direction = rl.vector2_subtract(player_position, self.position)
        bullet = self.create_bullet(direction, 300)
        bullet.position.x = self.position.x
        bullet.position.y = self.position.y
        self.bullets.append(bullet)


class ForkEmitter(BulletEmitter):
    def emit(self, **kwargs):
        super().emit(**kwargs)
        speed = kwargs.get("speed", 300)
        self.spawn_bullet(rl.Vector2(0.15, 1), speed)
        self.spawn_bullet(rl.Vector2(-0.15, 1), speed)

    def spawn_bullet(self, direction, speed):
        bullet = self.create_bullet(direction, speed)
        bullet.position.x = self.position.x
        bullet.position.y = self.position.y
        self.bullets.append(bullet)


class ShotgunEmitter(BulletEmitter):
    def __init__(self, bullets, texture, cd):
        super().__init__(bullets, texture, cd)

    def emit(self, **kwargs):
        super().emit(**kwargs)
        amount = kwargs.get("amount", 15)

        for _ in range(amount):
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            speed = random.randint(200, 300)
            bullet = self.create_bullet(rl.Vector2(dx, dy), speed)
            bullet.position.x = self.position.x
            bullet.position.y = self.position.y
            self.bullets.append(bullet)


class CircleEmitter(BulletEmitter):
    def __init__(self, bullets, texture, cd):
        super().__init__(bullets, texture, cd)

    def emit(self, **kwargs):
        super().emit(**kwargs)
        amount = kwargs.get("amount", 13)
        times = kwargs.get("times", 1)
        speed = kwargs.get("speed", 200)
        start_v = rl.Vector2(1, 0)

        for i in range(amount):
            for x in range(times):
                angle = math.radians((360 / amount) * i)
                direction = rl.vector2_rotate(start_v, angle)
                bullet = self.create_bullet(direction, speed + 50 * x)
                bullet.position.x = self.position.x
                bullet.position.y = self.position.y
                self.bullets.append(bullet)


# class SpiralEmitter(BulletEmitter):
#     def __init__(self, x: float, y: float, texture: rl.Texture):
#         super().__init__(x, y, texture)
#         self.emit_cooldown: float = 0
#         self.amount = 13
#         self.i = 0
#         self.start_v = rl.Vector2(1, 0)

#     def update(self, dt):
#         if self.emit_cooldown <= 0:
#             self.spawn_bullet(200)
#             self.spawn_bullet(400)

#             self.i += 1
#             if self.i >= self.amount:
#                 self.i = 0

#             self.emit_cooldown = 0.1

#         self.emit_cooldown -= dt

#         super().update(dt)

#     def spawn_bullet(self, speed):
#         angle = math.radians((360 / self.amount) * self.i)
#         direction = rl.vector2_normalize(rl.vector2_rotate(self.start_v, angle))
#         bullet = Bullet(Sprite(self.texture), direction, speed, BULLET_RADIUS)
#         bullet.position.x = self.position.x
#         bullet.position.y = self.position.y
#         self.bullets.append(bullet)

# class EternalMeek(BulletEmitter):
#     def __init__(self, x: float, y: float, texture: rl.Texture):
#         super().__init__(x, y, texture)
#         self.emit_cooldown: float = 0

#     def update(self, dt):
#         if self.emit_cooldown <= 0:
#             for _ in range(19):
#                 self.spawn_bullet()
#             self.emit_cooldown = 0.1

#         self.emit_cooldown -= dt

#         super().update(dt)

#     def spawn_bullet(self):
#         direction = rl.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
#         speed = random.randint(550, 590)
#         bullet = Bullet(Sprite(self.texture), direction, speed, BULLET_RADIUS)
#         bullet.position.x = self.position.x
#         bullet.position.y = self.position.y
#         self.bullets.append(bullet)
