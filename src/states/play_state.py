import pyray as rl
import raylib
from src.asset_store import AssetStore
from src.stages import Stage1
from src.constants import AREA_WIDTH, AREA_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT
from src.common import StateMachine, State
from src.utils import print_center


class PlayState(State):
    def __init__(self, sm: StateMachine):
        super().__init__()
        self.sm = sm
        self.stage = Stage1()
        self.is_paused = False
        self.gui_bg_color = rl.Color(0, 40, 10, 255)
        self.pause_bg_color = rl.Color(0, 0, 0, 150)

        rl.play_music_stream(self.stage.music)
        rl.set_music_volume(self.stage.music, 0.5)

    def update(self, dt):
        if rl.is_key_pressed(raylib.KEY_ESCAPE):
            self.is_paused = not self.is_paused

        if not self.is_paused:
            rl.update_music_stream(self.stage.music)
            self.stage.update(dt)

            if self.stage.player.lives <= 0:
                rl.stop_music_stream(self.stage.music)
                self.sm.switch("end", score=self.stage.score)

    def draw(self):
        self.stage.draw()

        font = AssetStore.get("font")
        gui_x = AREA_WIDTH
        gui_y = 0
        gui_width = WINDOW_WIDTH - AREA_WIDTH
        gui_height = WINDOW_HEIGHT
        rl.draw_rectangle_v((gui_x, gui_y), (gui_width, gui_height), self.gui_bg_color)
        rl.draw_line_ex((gui_x, gui_y), (gui_x, gui_height), 2, rl.BLACK)

        rl.draw_text_ex(font, f"Score: {self.stage.score}", (gui_x + 8, gui_y + 5), 30, 3, rl.WHITE)
        rl.draw_text_ex(font, f"Lives: {self.stage.player.lives}", (gui_x + 8, gui_y + 35), 30, 3, rl.WHITE)
        rl.draw_text_ex(font, f"FPS: {rl.get_fps()}", (gui_x + 8, gui_height - 30), 30, 3, rl.GRAY)

        if self.is_paused:
            rl.draw_rectangle(0, 0, AREA_WIDTH, AREA_HEIGHT, self.pause_bg_color)
            print_center(font, "(Paused)", 40, AREA_HEIGHT // 2 - 50, rl.YELLOW, AREA_WIDTH)