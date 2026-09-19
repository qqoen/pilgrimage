import pyray as rl
from src.player import Player
from src.background import Background
from src.enemy import Enemy, Boss, Mob
from src.bonus import Bonus
from src.asset_store import AssetStore
from src.blast import Explosion
from src.constants import AREA_WIDTH, AREA_HEIGHT
from src.utils import update_list, draw_list, print_center
from src.bullet import Bullet
from src.data import ENEMIES, EnemyType
from src.bullet_emitter import *
from src.sprite import AnimatedSprite
from src.common import Timeline, Timer


class TitleCard:
    def __init__(self):
        self._title = ""
        self._count = 3

    def show(self, title):
        self._title = title

    def update(self, dt):
        if self._count <= 0:
            return

        self._count -= dt

    def draw(self):
        if self._count <= 0:
            return

        font = AssetStore.get("font")
        text = f"[{self._title}]"
        width = rl.measure_text_ex(font, text, 30, 3).x
        rl.draw_text_ex(font, text, (AREA_WIDTH - width - 10, AREA_HEIGHT - 30), 30, 3, rl.WHITE)


class Stage:
    def __init__(self, bg: Background, music: str, stage_name: str):
        self.music: rl.Music = AssetStore.get(music)
        self.stage_name = stage_name
        self.name_timer = Timer(2, True)

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
        self.bg = bg
        self.title_card = TitleCard()

    def update(self, dt):
        self.player.update(dt)
        self.bg.update(dt)
        self.tl.update(dt)

        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if enemy.is_hit(bullet):
                    bullet.is_destroyed = True
                    self.hit_enemy(enemy)

        self.check_player_collisions()

        update_list(self.enemies, dt)
        update_list(self.explosions, dt)
        update_list(self.bonuses, dt)
        update_list(self.enemy_bullets, dt)
        self.title_card.update(dt)
        self.name_timer.update(dt)

        if len(self.enemies) == 0:
            self.tl.start()

    def check_player_collisions(self):
        if not self.player.is_visible:
            return

        for bonus in self.bonuses:
            if bonus.is_hit(self.player):
                bonus.pick()
                self.score += bonus.score

        if self.player.is_invincible:
            return

        for enemy in self.enemies:
            if enemy.is_hit(self.player):
                enemy.is_destroyed = True
                self.hit_player()

        for bullet in self.enemy_bullets:
            if bullet.is_hit(self.player):
                bullet.is_destroyed = True
                self.hit_player()

    def hit_enemy(self, enemy: Enemy):
        bonuses = enemy.hit()
        self.bonuses.extend(bonuses)

        if enemy.is_destroyed:
            self.explosions.append(Explosion(enemy.x, enemy.y))
            self.score += enemy.score

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

        enemy = Mob(ENEMIES[type], self.create_emitter(ENEMIES[type]))
        enemy.x = x
        enemy.y = -50
        self.enemies.append(enemy)

    def spawn_boss(self, type: str, lane: int):
        max_lanes = 5
        x = (AREA_WIDTH // (max_lanes + 1)) * lane

        enemy = Boss(ENEMIES[type], self.enemy_bullets)
        enemy.move(x, -50)
        self.enemies.append(enemy)
        self.tl.stop()

    def create_emitter(self, enemy: EnemyType):
        match enemy["emitter"]:
            case "single": return SingleEmitter(self.enemy_bullets, "bullet", enemy["cooldown"], enemy["speed"] + 100)
            case "fork": return ForkEmitter(self.enemy_bullets, "bullet", enemy["cooldown"])
            case "shotgun": return ShotgunEmitter(self.enemy_bullets, "bullet", enemy["cooldown"])
            case "circle": return CircleEmitter(self.enemy_bullets, "bullet", enemy["cooldown"])
            case "boss1": return Boss1Emitter(self.enemy_bullets, "bullet", enemy["cooldown"])
            case _: return EmptyEmitter()

    def draw(self):
        rl.clear_background(rl.BLACK)
        self.bg.draw()

        draw_list(self.explosions)
        self.player.draw()
        draw_list(self.bonuses)
        draw_list(self.enemies)
        draw_list(self.enemy_bullets)

        self.title_card.draw()

        if not self.name_timer.finished:
            font = AssetStore.get("font")
            print_center(font, self.stage_name, 40, AREA_HEIGHT // 2, rl.WHITE, AREA_WIDTH)

    def show_title_card(self, title):
        self.title_card.show(title)