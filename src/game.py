import pyray as rl
from src.asset_store import AssetStore
from src.stage import Stage


class Game:
    def __init__(self):
        rl.set_sound_volume(AssetStore.get("shoot_sound"), 0.8)
        rl.play_music_stream(AssetStore.get("music"))

        self.stage = Stage()

    def update(self, dt: float):
        rl.update_music_stream(AssetStore.get("music"))

        self.stage.update(dt)

    def draw(self):
        self.stage.draw()

        rl.draw_text_ex(AssetStore.get("font"), f"Score: {self.stage.score}", (8, 5), 30, 3, rl.WHITE)
        rl.draw_text_ex(AssetStore.get("font"), f"Lives: {self.stage.player.lives}", (8, 35), 30, 3, rl.WHITE)
