import pyray as rl
import raylib
import random
from src.player import Player
from src.background import StarsBackground, ScrollingBackground
from src.enemy import Enemy, Bonus
from src.asset_store import AssetStore
from src.blast import Explosion
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.common import update_list, draw_list
from src.bullet_emitter import SingleEmitter, ForkEmitter
from src.bullet import Bullet


class Game:
    def __init__(self, song_name):
        self.song_name = song_name
        self.bg = StarsBackground()
        self.player = Player()
        self.player.x = WINDOW_WIDTH // 2
        self.player.y = WINDOW_HEIGHT - self.player.height

        self.enemies: list[Enemy] = []
        self.explosions: list[Explosion] = []
        self.bonuses: list[Bonus] = []
        self.enemy_bullets: list[Bullet] = []

        self.default_color = rl.Color(0, 25, 50, 255)
        self.slow_color = rl.Color(50, 0, 50, 255)
        self.bg_color = self.default_color

        self.bg2 = ScrollingBackground(AssetStore.get("bg2_texture"))

        self.enemy_cd: float = 0

        self.score = 0

        rl.set_sound_volume(AssetStore.get("shoot_sound"), 0.8)
        rl.play_music_stream(AssetStore.get("music"))

    def update(self, delta_time: float):
        dt = delta_time
        self.bg_color = self.default_color

        if rl.is_key_down(raylib.KEY_LEFT_SHIFT):
            dt /= 2
            self.bg_color = self.slow_color
            rl.set_music_pitch(AssetStore.get("music"), 0.6)
            rl.set_music_volume(AssetStore.get("music"), 0.75)
        else:
            rl.set_music_pitch(AssetStore.get("music"), 1.0)
            rl.set_music_volume(AssetStore.get("music"), 1.0)

        rl.update_music_stream(AssetStore.get("music"))

        self.bg2.update(dt)
        self.bg.update(dt)
        self.player.update(dt)

        if self.enemy_cd <= 0:
            x = random.randint(100, WINDOW_WIDTH - 100)
            self.spawn_enemy(x, -50, 200)
            # self.spawn_enemy(x, -100, 210)
            # self.spawn_enemy(x + 50, -50, 220)
            self.enemy_cd = 1

        self.enemy_cd -= dt

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

        update_list(self.enemies, dt)
        update_list(self.explosions, dt)
        update_list(self.bonuses, dt)
        update_list(self.enemy_bullets, dt)

    def draw(self):
        rl.clear_background(self.bg_color)

        self.bg2.draw()
        # self.bg.draw()
        self.player.draw()
        draw_list(self.explosions)
        draw_list(self.bonuses)
        draw_list(self.enemies)
        draw_list(self.enemy_bullets)

        rl.draw_text_ex(AssetStore.get("font"), f"Score: {self.score}", (5, 5), 30, 5, rl.WHITE)

        # rl.draw_text_ex(AssetStore.get("font"), f"[{self.song_name}]", (5, WINDOW_HEIGHT - 25), 20, 5, rl.WHITE)

    def spawn_enemy(self, x, y, speed):
        emitter = ForkEmitter(self.enemy_bullets, AssetStore.get("bullet"), 1)
        enemy = Enemy(AssetStore.get("enemy1_texture"), speed, 3, emitter)
        enemy.x = x
        enemy.y = y
        self.enemies.append(enemy)
