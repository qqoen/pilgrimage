import pyray as rl
from src.asset_store import AssetStore
from src.bullet import Bullet
from src.bullet_emitter import *
from .stage import Stage
from src.background import TiledBackground


class Stage2(Stage):
    def __init__(self):
        super().__init__(TiledBackground(["grass_bg", "grass2_bg", "grass3_bg"]), "stage2music", "Stage 2")

        # self.show_title_card("Spirits Forest")

        offset = 1

        def add(time, func):
            self.tl.add(offset + time, func)

        add(1, lambda: self.spawn("fairy", lane=1))
        add(1.5, lambda: self.spawn("fairy", lane=2))
        add(2, lambda: self.spawn("fairy", lane=3))
        add(2.5, lambda: self.spawn("fairy", lane=4))
        add(3, lambda: self.spawn("fairy", lane=5))
