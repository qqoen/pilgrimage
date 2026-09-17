import pyray as rl
import random
import math
from abc import ABC, abstractmethod
from src.bullet import Bullet
from src.sprite import Sprite


class BulletEmitter(ABC):
    def __init__(self, bullets: list[Bullet], texture: rl.Texture, emit_cooldown: float):
        self.bullets = bullets
        self.position = rl.Vector2()
        self.texture = texture
        self.emit_cooldown = emit_cooldown
        self.emit_timer: float = 0

    def update(self, dt: float):
        if self.emit_timer <= 0:
            self.emit()
            self.emit_timer = self.emit_cooldown

        self.emit_timer -= dt

    @abstractmethod
    def emit(self):
        pass


class SingleEmitter(BulletEmitter):
    def emit(self):
        direction = rl.Vector2(0, 1)
        bullet = Bullet(Sprite(self.texture, 1), direction, 450, 6)
        bullet.position.x = self.position.x
        bullet.position.y = self.position.y
        self.bullets.append(bullet)


class ForkEmitter(BulletEmitter):
    def emit(self):
        self.spawn_bullet(rl.Vector2(0.5, 1))
        self.spawn_bullet(rl.Vector2(-0.5, 1))

    def spawn_bullet(self, direction):
        bullet = Bullet(Sprite(self.texture, 1), rl.vector2_normalize(direction), 450, 6)
        bullet.position.x = self.position.x
        bullet.position.y = self.position.y
        self.bullets.append(bullet)


# class Shotgun(BulletEmitter):
#     def __init__(self, x: float, y: float, texture: rl.Texture):
#         super().__init__(x, y, texture)
#         self.emit_cooldown: float = 0

#     def update(self, dt):
#         if self.emit_cooldown <= 0:
#             for _ in range(50):
#                 dx = random.uniform(-1, 1)
#                 dy = random.uniform(-1, 1)
#                 direction = rl.Vector2(dx, dy)
#                 bullet = Bullet(Sprite(self.texture), direction, 400, 5)
#                 bullet.position.x = self.position.x
#                 bullet.position.y = self.position.y
#                 self.bullets.append(bullet)

#             self.emit_cooldown = 1

#         self.emit_cooldown -= 1 * dt

#         super().update(dt)


# class CircleEmitter(BulletEmitter):
#     def __init__(self, x: float, y: float, texture: rl.Texture):
#         super().__init__(x, y, texture)
#         self.emit_cooldown: float = 0

#     def update(self, dt):
#         if self.emit_cooldown <= 0:
#             amount = 13
#             start_v = rl.Vector2(1, 0)

#             for i in range(amount):
#                 for x in range(3):
#                     angle = math.radians((360 / amount) * i)
#                     direction = rl.vector2_normalize(rl.vector2_rotate(start_v, angle))

#                     bullet = Bullet(Sprite(self.texture), direction, 200 + 50 * x, 5)
#                     bullet.position.x = self.position.x
#                     bullet.position.y = self.position.y
#                     self.bullets.append(bullet)

#             self.emit_cooldown = 1

#         self.emit_cooldown -= 1 * dt

#         super().update(dt)


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
#         bullet = Bullet(Sprite(self.texture), direction, speed, 5)
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
#         bullet = Bullet(Sprite(self.texture), direction, speed, 5)
#         bullet.position.x = self.position.x
#         bullet.position.y = self.position.y
#         self.bullets.append(bullet)
