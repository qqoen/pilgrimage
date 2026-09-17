import pyray as rl
import raylib
from src.asset_store import AssetStore
from src.stage import Stage1
from src.constants import AREA_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT
from src.state_machine import StateMachine, State


class StartState(State):
    def __init__(self, sm: StateMachine):
        self.sm = sm

    def update(self, dt):
        if rl.is_key_pressed(raylib.KEY_ENTER):
            self.sm.switch("play")

    def draw(self):
        # rl.clear_background(rl.BLACK)
        rl.draw_text("Press Enter to start", WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 30, rl.WHITE)


class PlayState(State):
    def __init__(self, sm: StateMachine):
        super().__init__()
        self.sm = sm
        self.stage = Stage1()
        rl.play_music_stream(AssetStore.get("music"))

    def update(self, dt):
        rl.update_music_stream(AssetStore.get("music"))
        self.stage.update(dt)

        if self.stage.player.lives <= 0:
            rl.stop_music_stream(AssetStore.get("music"))
            self.sm.switch("start")

    def draw(self):
        self.stage.draw()

        gui_x = AREA_WIDTH
        gui_y = 0
        gui_width = WINDOW_WIDTH - AREA_WIDTH
        gui_height = WINDOW_HEIGHT
        rl.draw_rectangle_v((gui_x, gui_y), (gui_width, gui_height), rl.BLACK)

        rl.draw_text_ex(AssetStore.get("font"), f"Score: {self.stage.score}", (gui_x + 8, gui_y + 5), 30, 3, rl.WHITE)
        rl.draw_text_ex(AssetStore.get("font"), f"Lives: {self.stage.player.lives}", (gui_x + 8, gui_y + 35), 30, 3, rl.WHITE)

        rl.draw_text_ex(AssetStore.get("font"), f"FPS: {rl.get_fps()}", (gui_x + 8, gui_height - 30), 30, 3, rl.GRAY)


class Game(StateMachine):
    def __init__(self):
        super().__init__()
        rl.set_sound_volume(AssetStore.get("shoot_sound"), 0.8)

        self.register("start", lambda _: StartState(self))
        self.register("play", lambda _: PlayState(self))

        self.switch("start")
