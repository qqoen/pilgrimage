import pyray as rl
import raylib
from src.game_object import GameObject
from src.asset_store import AssetStore
from src.sprite import Sprite, AnimatedSprite
from src.bullet import Bullet
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from src.common import approach, play_sound, draw_list, update_list


class Player(GameObject):
    def __init__(self, sprite: AnimatedSprite):
        super().__init__(sprite, 5)
        self.bullet_sprite = Sprite(AssetStore.get("player_bullet"), 3, rl.GRAY)
        self.trail = Sprite(AssetStore.get("player1"), 3, rl.GRAY)
        self.trail_position = rl.Vector2()
        self.speed = 410
        self.bullets: list[Bullet] = []
        self.shot_cooldown: float = 0
        self.lives = 3

    @GameObject.x.setter
    def x(self, value):
        self.position.x = value
        self.trail_position.x = self.position.x

    @GameObject.y.setter
    def y(self, value):
        self.position.y = value
        self.trail_position.y = self.position.y

    def update(self, dt: float):
        dir = rl.Vector2(0, 0)
        dir.x = int(rl.is_key_down(raylib.KEY_RIGHT)) - int(rl.is_key_down(raylib.KEY_LEFT))
        dir.y = int(rl.is_key_down(raylib.KEY_DOWN)) - int(rl.is_key_down(raylib.KEY_UP))
        dir = rl.vector2_scale(rl.vector2_normalize(dir), self.speed * dt)
        self.position = rl.vector2_add(self.position, dir)

        self.position.x = rl.clamp(self.position.x, self.width() // 3, WINDOW_WIDTH - self.width() // 3)
        self.position.y = rl.clamp(self.position.y, self.height() // 3, WINDOW_HEIGHT - self.height() // 3)

        self.trail_position.x = approach(self.trail_position.x, self.position.x)
        self.trail_position.y = approach(self.trail_position.y, self.position.y)

        if rl.is_key_down(raylib.KEY_Z) and self.shot_cooldown <= 0:
            self.spawn_bullet(self.position.x - 14, self.position.y - self.height() // 2)
            self.spawn_bullet(self.position.x + 14, self.position.y - self.height() // 2)
            self.shot_cooldown = 0.1
            play_sound(AssetStore.get("shoot_sound"))

        self.shot_cooldown -= dt

        update_list(self.bullets, dt)

        self.sprite.update(dt)

    def spawn_bullet(self, x, y):
        bullet = Bullet(self.bullet_sprite, rl.Vector2(0, -1), self.speed + 100, 6)
        bullet.position.x = x
        bullet.position.y = y
        self.bullets.append(bullet)

    def draw(self):
        self.trail.draw(self.trail_position.x, self.trail_position.y)
        super().draw()
        draw_list(self.bullets)
