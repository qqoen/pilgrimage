import pyray as rl
from src.asset_store import AssetStore
from src.states import StartState, PlayState, EndState
from src.common import StateMachine


class PlayerData:
    def __init__(self):
        self._highscore = 0

    @property
    def highscore(self):
        return self._highscore

    def update_score(self, new_score):
        self._highscore = max(self._highscore, new_score)


class Game(StateMachine):
    def __init__(self):
        super().__init__()
        rl.set_sound_volume(AssetStore.get("shoot_sound"), 0.8)

        player_data = PlayerData()

        self.register("start", lambda _: StartState(self, player_data))
        self.register("play", lambda _: PlayState(self))
        self.register("end", lambda pl: EndState(self, player_data, pl["score"]))

        self.switch("start")
