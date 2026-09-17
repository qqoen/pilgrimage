import pyray as rl
import raylib
from src.asset_store import AssetStore
from src.state_machine import StateMachine
from src.start_state import StartState
from src.play_state import PlayState
from src.end_state import EndState


class Game(StateMachine):
    def __init__(self):
        super().__init__()
        rl.set_sound_volume(AssetStore.get("shoot_sound"), 0.8)

        self.register("start", lambda _: StartState(self))
        self.register("play", lambda _: PlayState(self))
        self.register("end", lambda pl: EndState(self, pl["score"]))

        self.switch("start")
