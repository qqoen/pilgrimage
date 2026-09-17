import pyray as rl
import raylib
from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.state_machine import StateMachine, State
from src.asset_store import AssetStore
from src.common import print_center


class StartState(State):
    def __init__(self, sm: StateMachine):
        self.sm = sm

    def update(self, dt):
        if rl.is_key_pressed(raylib.KEY_ENTER):
            self.sm.switch("play")

    def draw(self):
        rl.clear_background(rl.BLACK)
        font = AssetStore.get("font")
        print_center(font, "Pilgrimage", 60, 10, rl.BLUE)
        print_center(font, "Press Enter to start", 30, 100, rl.GRAY)
        print_center(font, "Press Escape to quit", 30, 130, rl.GRAY)
        print_center(font, "2026", 25, WINDOW_HEIGHT - 40)
