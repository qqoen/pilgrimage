import pyray as rl
import random
from src.player import Player
from src.background import ScrollingBackground
from src.enemy import Enemy, Bonus
from src.asset_store import AssetStore
from src.blast import Explosion
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.common import update_list, draw_list
from src.bullet import Bullet
from src.data import ENEMIES, EnemyType
from src.bullet_emitter import ForkEmitter, EmptyEmitter
from src.sprite import AnimatedSprite


class Timeline:
    def __init__(self):
        self.time = 0.0
        self.events = {}

    def update(self, dt):
        self.time += dt
        expired = []

        for (t, callback) in self.events.items():
            if t <= self.time:
                callback()
                expired.append(t)

        for t in expired:
            self.events.pop(t)

    def add(self, time, callback):
        if time in self.events:
            raise ValueError(f"Time '{time}' already exists on timeline.")

        self.events[time] = callback


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

        self.timeline = Timeline()

        self.timeline.add(1, lambda: self.spawn_enemy("fairy", 100))
        self.timeline.add(2, lambda: self.spawn_enemy("fairy", 150))
        self.timeline.add(3, lambda: self.spawn_enemy("fairy", 200))

        self.timeline.add(5, lambda: self.spawn_enemy("fairy", WINDOW_WIDTH - 100))
        self.timeline.add(6, lambda: self.spawn_enemy("fairy", WINDOW_WIDTH - 150))
        self.timeline.add(7, lambda: self.spawn_enemy("fairy", WINDOW_WIDTH - 200))

        self.bg = ScrollingBackground(AssetStore.get("bg2_texture"))

    def update(self, dt):
        self.player.update(dt)
        self.bg.update(dt)

        self.timeline.update(dt)

        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if enemy.is_hit(bullet):
                    bonuses = enemy.hit()
                    bullet.is_destroyed = True

                    self.bonuses.extend(bonuses)

                    if enemy.is_destroyed:
                        self.explosions.append(Explosion(enemy.x, enemy.y))
                        self.score += 30

        for bonus in self.bonuses:
            if bonus.is_hit(self.player):
                bonus.pick()
                self.score += bonus.score

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

    def hit_player(self):
        self.player.lives -= 1
        self.reset_player()

    def reset_player(self):
        self.player.x = WINDOW_WIDTH // 2
        self.player.y = WINDOW_HEIGHT - self.player.height()

    def spawn_enemy(self, type: str, x):
        enemy = Enemy(ENEMIES[type], self.create_emitter(ENEMIES[type]))
        enemy.x = x
        enemy.y = -50
        self.enemies.append(enemy)

    def create_emitter(self, enemy: EnemyType):
        if enemy["emitter"] == "fork":
            return ForkEmitter(self.enemy_bullets, "bullet", 1)

        return EmptyEmitter()

    def draw(self):
        self.bg.draw()

        draw_list(self.explosions)
        self.player.draw()
        draw_list(self.bonuses)
        draw_list(self.enemies)
        draw_list(self.enemy_bullets)