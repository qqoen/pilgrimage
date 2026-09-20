import pyray as rl
from src.asset_store import AssetStore
from src.bullet import Bullet
from src.bullet_emitter import *
from .stage import Stage
from src.background import TiledBackground


class Stage1(Stage):
    def __init__(self):
        super().__init__(TiledBackground(["grass_bg", "grass2_bg", "grass3_bg"]), "stage3music", "Stage 1")

        # self.show_title_card("Spirits Forest")

        offset = 1

        def add(time, func):
            self.tl.add(offset + time, func)

        add(1, lambda: self.spawn("fairy", lane=1))
        add(1.5, lambda: self.spawn("fairy", lane=2))
        add(2, lambda: self.spawn("fairy", lane=3))
        add(2.5, lambda: self.spawn("fairy", lane=4))
        add(3, lambda: self.spawn("fairy", lane=5))

        # add(5, lambda: self.spawn("fairy", lane=5))
        # add(5.5, lambda: self.spawn("fairy", lane=4))
        # add(6, lambda: self.spawn("fairy", lane=3))
        # add(6.5, lambda: self.spawn("fairy", lane=2))
        # add(7, lambda: self.spawn("fairy", lane=1))

        # add(10, lambda: self.spawn("fairy2", lane=1))
        # add(11, lambda: self.spawn("fairy2", lane=5))

        # add(14, lambda: self.spawn("fairy", lane=1))
        # add(14.5, lambda: self.spawn("fairy", lane=2))
        # add(15, lambda: self.spawn("fairy", lane=1))
        # add(15.5, lambda: self.spawn("fairy", lane=2))

        # add(17, lambda: self.spawn("fairy", lane=5))
        # add(17.5, lambda: self.spawn("fairy", lane=4))
        # add(18, lambda: self.spawn("fairy", lane=5))
        # add(18.5, lambda: self.spawn("fairy", lane=4))
        # add(19, lambda: self.spawn("fairy", lane=5))

        # add(21, lambda: self.spawn("fairy2", lane=1))
        # add(22, lambda: self.spawn("fairy2", lane=3))
        # add(23, lambda: self.spawn("fairy2", lane=5))

        # add(28, lambda: self.spawn_boss("boss1", lane=3))

        # add(31, lambda: self.spawn("fairy", lane=1))
        # add(31.5, lambda: self.spawn("fairy", lane=2))
        # add(32, lambda: self.spawn("fairy", lane=3))
        # add(32.5, lambda: self.spawn("fairy", lane=4))

        # add(34, lambda: self.spawn("fairy", lane=5))
        # add(34.5, lambda: self.spawn("fairy", lane=4))
        # add(35, lambda: self.spawn("fairy", lane=3))
        # add(35.5, lambda: self.spawn("fairy", lane=2))

        # add(37, lambda: self.spawn("fairy2", lane=5))
        # add(37.5, lambda: self.spawn("fairy2", lane=1))

        # add(38.5, lambda: self.spawn("fairy", lane=4))
        # add(39, lambda: self.spawn("fairy", lane=2))
        # add(39.5, lambda: self.spawn("fairy", lane=4))
        # add(40, lambda: self.spawn("fairy", lane=2))
