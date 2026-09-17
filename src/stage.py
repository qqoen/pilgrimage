import pyray as rl
import random
from src.player import Player
from src.background import ScrollingBackground
from src.enemy import Enemy, Bonus
from src.asset_store import AssetStore
from src.blast import Explosion
from src.constants import AREA_WIDTH, AREA_HEIGHT
from src.common import update_list, draw_list, play_sound
from src.bullet import Bullet
from src.data import ENEMIES, EnemyType
from src.bullet_emitter import ForkEmitter, EmptyEmitter, ShotgunEmitter
from src.sprite import AnimatedSprite


class Timeline:
    def __init__(self):
        self._time = 0.0
        self._events = []

    def update(self, dt):
        self._time += dt

        for i, (t, callback) in enumerate(self._events):
            if t <= self._time:
                callback()
                del self._events[i]

    def add(self, time, callback):
        self._events.append((time, callback))


class Stage:
    def __init__(self):
        player_sprite = AnimatedSprite([
            "player1",
            "player2",
            "player3",
            "player4",
        ], 0.25, 3)
        self.player = Player(player_sprite)
        self.reset_player()
        self.enemies: list[Enemy] = []
        self.enemy_bullets: list[Bullet] = []
        self.explosions: list[Explosion] = []
        self.bonuses: list[Bonus] = []
        self.score = 0
        self.tl = Timeline()
        self.bg = ScrollingBackground(AssetStore.get("bg2_texture"))

    def update(self, dt):
        self.player.update(dt)
        self.bg.update(dt)
        self.tl.update(dt)

        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if enemy.is_hit(bullet):
                    bullet.is_destroyed = True
                    self.hit_enemy(enemy)

        for bonus in self.bonuses:
            if bonus.is_hit(self.player):
                bonus.pick()
                self.score += bonus.score

        if self.player.respawn_timer <= 0:
            for enemy in self.enemies:
                if enemy.is_hit(self.player):
                    enemy.is_destroyed = True
                    self.hit_player()

            for bullet in self.enemy_bullets:
                if bullet.is_hit(self.player):
                    bullet.is_destroyed = True
                    self.hit_player()

        update_list(self.enemies, dt)
        update_list(self.explosions, dt)
        update_list(self.bonuses, dt)
        update_list(self.enemy_bullets, dt)

    def hit_enemy(self, enemy: Enemy):
        bonuses = enemy.hit()
        self.bonuses.extend(bonuses)

        if enemy.is_destroyed:
            self.explosions.append(Explosion(enemy.x, enemy.y))
            self.score += 30

    def hit_player(self):
        self.player.hit()
        self.explosions.append(Explosion(self.player.x, self.player.y))
        self.reset_player()

    def reset_player(self):
        self.player.x = AREA_WIDTH // 2
        self.player.y = AREA_HEIGHT - self.player.height()

    def spawn(self, type: str, lane: int):
        max_lanes = 5
        x = (AREA_WIDTH // (max_lanes + 1)) * lane

        enemy = Enemy(ENEMIES[type], self.create_emitter(ENEMIES[type]))
        enemy.x = x
        enemy.y = -50
        self.enemies.append(enemy)

    def create_emitter(self, enemy: EnemyType):
        match enemy["emitter"]:
            case "fork": return ForkEmitter(self.enemy_bullets, "bullet", 1)
            case "shotgun": return ShotgunEmitter(self.enemy_bullets, "bullet", 2)
            case _: return EmptyEmitter()

    def draw(self):
        self.bg.draw()

        draw_list(self.explosions)
        self.player.draw()
        draw_list(self.bonuses)
        draw_list(self.enemies)
        draw_list(self.enemy_bullets)


class Stage1(Stage):
    def __init__(self):
        super().__init__()

        self.tl.add(1, lambda: self.spawn("fairy", lane=1))
        self.tl.add(2, lambda: self.spawn("fairy", lane=2))
        self.tl.add(3, lambda: self.spawn("fairy", lane=3))
        self.tl.add(4, lambda: self.spawn("fairy", lane=4))
        self.tl.add(5, lambda: self.spawn("fairy", lane=5))

        self.tl.add(7, lambda: self.spawn("fairy", lane=5))
        self.tl.add(8, lambda: self.spawn("fairy", lane=4))
        self.tl.add(9, lambda: self.spawn("fairy", lane=3))
        self.tl.add(10, lambda: self.spawn("fairy", lane=2))
        self.tl.add(11, lambda: self.spawn("fairy", lane=1))
        self.tl.add(12, lambda: self.spawn("fairy", lane=2))
        self.tl.add(13, lambda: self.spawn("fairy", lane=1))

        self.tl.add(15, lambda: self.spawn("fairy2", lane=1))
        self.tl.add(16, lambda: self.spawn("fairy2", lane=5))

        self.tl.add(19, lambda: self.spawn("fairy", lane=1))
        self.tl.add(19.5, lambda: self.spawn("fairy", lane=2))
        self.tl.add(20, lambda: self.spawn("fairy", lane=1))
        self.tl.add(20.5, lambda: self.spawn("fairy", lane=2))

        self.tl.add(22, lambda: self.spawn("fairy", lane=5))
        self.tl.add(22.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(23, lambda: self.spawn("fairy", lane=5))
        self.tl.add(23.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(24, lambda: self.spawn("fairy", lane=5))

        self.tl.add(26, lambda: self.spawn("fairy2", lane=5))
        self.tl.add(27, lambda: self.spawn("fairy2", lane=1))
        self.tl.add(28, lambda: self.spawn("fairy2", lane=3))
