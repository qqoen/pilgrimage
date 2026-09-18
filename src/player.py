import pyray as rl
import raylib
from src.game_object import GameObject
from src.asset_store import AssetStore
from src.sprite import Sprite, AnimatedSprite
from src.bullet import Bullet
from src.constants import AREA_WIDTH, AREA_HEIGHT
from src.utils import play_sound, draw_list, update_list
from src.common import Timer


class Option:
    def __init__(self, offset):
        self.position = rl.Vector2()
        self.offset = offset
        self.speed = 320

    def update(self, dt, target: rl.Vector2):
        self.position = rl.vector2_move_towards(self.position, target, self.speed * dt)

    def draw(self):
        x = self.position.x + self.offset
        y = self.position.y
        rl.draw_circle_v((x, y), 10, rl.RED)


class Trail:
    def __init__(self):
        self.sprite = Sprite(AssetStore.get("player1"), 3, rl.fade(rl.WHITE, 0.5))
        self.position = rl.Vector2()
        self.speed = 320

    def update(self, dt, target: rl.Vector2):
        self.position = rl.vector2_move_towards(self.position, target, self.speed * dt)

    def draw(self):
        self.sprite.draw(self.position.x, self.position.y)


class Player(GameObject):
    def __init__(self, sprite: AnimatedSprite):
        super().__init__(sprite, 6)
        self.bullet_sprite = Sprite(AssetStore.get("player_bullet"), 3, rl.GRAY)
        self.speed = 410
        self.bullets: list[Bullet] = []
        self.shot_cooldown: float = 0
        self.lives = 3
        self.trail = Trail()

        self.left_opt = Option(-55)
        self.right_opt = Option(55)

        self._respawn_timer = Timer(1.0)

    @GameObject.x.setter
    def x(self, value):
        self.position.x = value
        self.trail.position.x = self.position.x
        self.left_opt.position.x = self.position.x
        self.right_opt.position.x = self.position.x

    @GameObject.y.setter
    def y(self, value):
        self.position.y = value
        self.trail.position.y = self.position.y
        self.left_opt.position.y = self.position.y
        self.right_opt.position.y = self.position.y

    @property
    def is_visible(self):
        return self._respawn_timer.finished

    def update(self, dt: float):
        self.shot_cooldown -= dt
        update_list(self.bullets, dt)

        if not self._respawn_timer.finished:
            self._respawn_timer.update(dt)
            return

        self.move_player(dt)

        self.left_opt.update(dt, self.position)
        self.right_opt.update(dt, self.position)
        self.trail.update(dt, self.position)

        if rl.is_key_down(raylib.KEY_Z) and self.shot_cooldown <= 0:
            self.spawn_bullet(self.position.x - 14, self.position.y - self.height() // 2)
            self.spawn_bullet(self.position.x + 14, self.position.y - self.height() // 2)
            self.shot_cooldown = 0.1
            play_sound(AssetStore.get("shoot_sound"))

        self.sprite.update(dt)

    def move_player(self, dt):
        dir = rl.Vector2(0, 0)
        dir.x = int(rl.is_key_down(raylib.KEY_RIGHT)) - int(rl.is_key_down(raylib.KEY_LEFT))
        dir.y = int(rl.is_key_down(raylib.KEY_DOWN)) - int(rl.is_key_down(raylib.KEY_UP))

        speed = self.speed

        if rl.is_key_down(raylib.KEY_LEFT_SHIFT):
            speed = self.speed * 0.6

        dir = rl.vector2_scale(rl.vector2_normalize(dir), speed * dt)
        self.position = rl.vector2_add(self.position, dir)
        self.position.x = rl.clamp(self.position.x, self.width() // 3, AREA_WIDTH - self.width() // 3)
        self.position.y = rl.clamp(self.position.y, self.height() // 3, AREA_HEIGHT - self.height() // 3)

    def spawn_bullet(self, x, y):
        bullet = Bullet(self.bullet_sprite, rl.Vector2(0, -1), self.speed + 100, 6)
        bullet.position.x = x
        bullet.position.y = y
        self.bullets.append(bullet)

    def hit(self):
        self.lives -= 1
        self._respawn_timer.start()
        play_sound(AssetStore.get("destroy_sound"))

    def draw(self):
        if self._respawn_timer.finished:
            self.trail.draw()
            super().draw()

            if rl.is_key_down(raylib.KEY_LEFT_SHIFT):
                rl.draw_circle_v(self.position, self.hit_radius + 2, rl.BLACK)
                rl.draw_circle_v(self.position, self.hit_radius, rl.WHITE)

            # self.left_opt.draw()
            # self.right_opt.draw()

        draw_list(self.bullets)
