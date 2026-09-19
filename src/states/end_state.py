import pyray as rl
import raylib
from src.asset_store import AssetStore
from src.common import StateMachine, State


class EndState(State):
    def __init__(self, sm: StateMachine, player_data, score):
        super().__init__()
        self.sm = sm
        self.player_data = player_data
        self.score = score

    def update(self, dt):
        if rl.is_key_pressed(raylib.KEY_ENTER):
            self.player_data.update_score(self.score)
            self.sm.switch("start")

    def draw(self):
        rl.clear_background(rl.BLACK)
        font = AssetStore.get("font")
        rl.draw_text_ex(font, f"Final score: {self.score}", (10, 10), 30, 3, rl.WHITE)
        rl.draw_text_ex(font, "Press Enter to continue", (10, 40), 30, 3, rl.WHITE)
