import pyray as rl
import random
from src.utils import play_sound
from src.asset_store import AssetStore
from src.sprite import Sprite, Shadow
from src.bonus import Bonus
from src.game_object import GameObject
from src.constants import AREA_WIDTH, AREA_HEIGHT
from src.data import EnemyType
from src.bullet_emitter import *
from src.common import TimelineLoop


class Enemy(GameObject):
    def __init__(self, enemy: EnemyType):
        super().__init__(Sprite(AssetStore.get(enemy["texture"]), 3), 16)
        self.enemy_data = enemy
        self.speed = enemy["speed"]
        self.health = enemy["health"]
        self.hit_frames = 0.0
        self.bonus_chance = enemy["bonus_chance"]
        self.bonus_count = max(1, enemy["bonus_count"])
        self.score = enemy["score"]
        self.shadow = Shadow(enemy["texture"], 3)

    def update(self, dt):
        if self.hit_frames > 0:
            self.sprite.tint = rl.RED
            self.hit_frames -= 25 * dt
        else:
            self.sprite.tint = rl.WHITE
            self.hit_frames = 0

        self.shadow.update(dt, self.position)

    def draw(self):
        self.shadow.draw()
        super().draw()

    def hit(self) -> list[Bonus]:
        if self.is_destroyed or self.y < self.height():
            return []

        self.health -= 1
        self.on_hit()
        bonuses = []

        if self.health <= 0:
            play_sound(AssetStore.get("destroy_sound"))
            self.is_destroyed = True

            count = random.randint(1, self.bonus_count)

            for _ in range(count):
                if random.randint(1, 100) <= self.bonus_chance:
                    x = self.x + random.randint(-20, 20)
                    y = self.y + random.randint(-20, 20)
                    bonuses.append(Bonus(x, y, self.score))
        else:
            play_sound(AssetStore.get("hit_sound"))
            self.hit_frames = 1

        return bonuses

    def on_hit(self):
        pass


class Mob(Enemy):
    def __init__(self, enemy: EnemyType, emitter: BulletEmitter):
        super().__init__(enemy)
        self.emitter = emitter
        self.x_dir = random.choice([-1, 1])

    @GameObject.x.setter
    def x(self, value):
        self.position.x = value
        self.emitter.position.x = value

    @GameObject.y.setter
    def y(self, value):
        self.position.y = value
        self.emitter.position.y = value

    def update(self, dt: float):
        super().update(dt)
        self.y += self.speed * dt

        if self.enemy_data["behavior"] == "move":
            if self.x >= AREA_WIDTH - self.width():
                self.x_dir = -1
            elif self.x <= self.width():
                self.x_dir = 1

            self.x += self.x_dir * (self.speed // 2) * dt

        if 0 < self.position.y < (AREA_HEIGHT // 3) * 2:
            self.emitter.update(dt)

        if self.position.y >= AREA_HEIGHT:
            self.is_destroyed = True

    def on_hit(self):
        self.x += random.randint(-3, 3)


class Boss(Enemy):
    INIT = 0
    ATTACK = 1

    def __init__(self, enemy: EnemyType, bullets: list[Bullet]):
        super().__init__(enemy)
        self.max_health = enemy["health"]
        self.state = Boss.INIT
        self.target = rl.Vector2()

        self.shotgun_emitter = ShotgunEmitter(bullets, "bullet", 0)
        self.circle_emitter = CircleEmitter(bullets, "bullet", 0)

        self.tl = TimelineLoop(2.5)

        self.tl.add(0, lambda: self.circle_emitter.emit(amount=13, times=2, speed=150))
        self.tl.add(0.5, lambda: self.circle_emitter.emit(amount=14, times=2, speed=200))
        self.tl.add(1, lambda: self.shotgun_emitter.emit(amount=40))
        self.tl.add(1.5, lambda: self.move_random())

    def move(self, x, y):
        self.position.x = x
        self.position.y = y
        self.target.x = x
        self.target.y = y

    def move_random(self):
        self.target.x = random.randint(50, AREA_WIDTH - 50)
        self.target.y = self.position.y

    def update(self, dt: float):
        super().update(dt)

        if self.state == Boss.INIT:
            y = self.y + self.speed * dt
            self.move(self.x, y)

            if self.y > AREA_HEIGHT // 3:
                self.state = Boss.ATTACK
        elif self.state == Boss.ATTACK:
            self.tl.update(dt)
            self.position = rl.vector2_move_towards(self.position, self.target, self.speed * dt)

        self.shotgun_emitter.move(self.position.x, self.position.y)
        self.circle_emitter.move(self.position.x, self.position.y)

    def hit(self):
        if self.state == Boss.INIT:
            return []

        return super().hit()

    def draw(self):
        super().draw()
        font = AssetStore.get("font")
        # rl.draw_text_ex(font, f"HP: {self.health}/{self.max_health}", (10, 10), 30, 3, rl.WHITE)

        ratio = self.health / self.max_health
        bar_width = AREA_WIDTH - 20
        rl.draw_rectangle(10, 10, bar_width, 6, rl.GRAY)
        rl.draw_rectangle(10, 10, int(bar_width * ratio), 6, rl.WHITE)
