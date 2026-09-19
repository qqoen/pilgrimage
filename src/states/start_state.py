import pyray as rl
import raylib
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.common import StateMachine, State
from src.asset_store import AssetStore
from src.utils import print_center


class StartState(State):
    def __init__(self, sm: StateMachine, player_data):
        self.sm = sm
        self.player_data = player_data

    def update(self, dt):
        if rl.is_key_pressed(raylib.KEY_ENTER):
            self.sm.switch("play")

    def draw(self):
        rl.clear_background(rl.BLACK)
        font = AssetStore.get("font")
        print_center(font, "Pilgrimage", 60, 10, rl.BLUE)

        if self.player_data.highscore > 0:
            print_center(font, f"Highscore: {self.player_data.highscore}", 35, 100, rl.YELLOW)

        print_center(font, "Press Enter to start", 30, 150, rl.GRAY)
        print_center(font, "Press Escape to quit", 30, 180, rl.GRAY)
        print_center(font, "2026", 25, WINDOW_HEIGHT - 40)
