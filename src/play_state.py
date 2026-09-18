import pyray as rl
from src.asset_store import AssetStore
from src.stage import Stage1
from src.constants import AREA_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT
from src.state_machine import StateMachine, State


class PlayState(State):
    def __init__(self, sm: StateMachine):
        super().__init__()
        self.sm = sm
        self.stage = Stage1()
        rl.play_music_stream(self.stage.music)
        rl.set_music_volume(self.stage.music, 0.5)

        self.gui_bg_color = rl.Color(0, 40, 10, 255)

    def update(self, dt):
        rl.update_music_stream(self.stage.music)
        self.stage.update(dt)

        if self.stage.player.lives <= 0:
            rl.stop_music_stream(self.stage.music)
            self.sm.switch("end", score=self.stage.score)

    def draw(self):
        self.stage.draw()

        gui_x = AREA_WIDTH
        gui_y = 0
        gui_width = WINDOW_WIDTH - AREA_WIDTH
        gui_height = WINDOW_HEIGHT
        rl.draw_rectangle_v((gui_x, gui_y), (gui_width, gui_height), self.gui_bg_color)
        rl.draw_line_ex((gui_x, gui_y), (gui_x, gui_height), 2, rl.BLACK)

        font = AssetStore.get("font")
        rl.draw_text_ex(font, f"Score: {self.stage.score}", (gui_x + 8, gui_y + 5), 30, 3, rl.WHITE)
        rl.draw_text_ex(font, f"Lives: {self.stage.player.lives}", (gui_x + 8, gui_y + 35), 30, 3, rl.WHITE)
        rl.draw_text_ex(font, f"FPS: {rl.get_fps()}", (gui_x + 8, gui_height - 30), 30, 3, rl.GRAY)