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
        self.menu_idx = 0

    def update(self, dt):
        if rl.is_key_pressed(raylib.KEY_DOWN):
            self.menu_idx += 1
        elif rl.is_key_pressed(raylib.KEY_UP):
            self.menu_idx -= 1

        if rl.is_key_pressed(raylib.KEY_ENTER):
            if self.menu_idx == 0:
                self.sm.switch("play")
            elif self.menu_idx == 1:
                self.sm.switch("survival")
            elif self.menu_idx == 2:
                self.player_data.should_quit = True

        self.menu_idx = int(rl.clamp(self.menu_idx, 0, 2))

    def draw(self):
        rl.clear_background(rl.BLACK)
        font = AssetStore.get("font")
        print_center(font, "Pilgrimage", 60, 10, rl.BLUE)

        if self.player_data.highscore > 0:
            print_center(font, f"Highscore: {self.player_data.highscore}", 35, 100, rl.YELLOW)

        print_center(font, "Arcade mode", 30, 150, rl.WHITE if self.menu_idx == 0 else rl.GRAY)
        print_center(font, "Survival mode", 30, 180, rl.WHITE if self.menu_idx == 1 else rl.GRAY)
        print_center(font, "Quit", 30, 210, rl.WHITE if self.menu_idx == 2 else rl.GRAY)

        print_center(font, "2026", 25, WINDOW_HEIGHT - 40)
