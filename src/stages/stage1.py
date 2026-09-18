import pyray as rl
from src.asset_store import AssetStore
from src.bullet import Bullet
from src.bullet_emitter import *
from .stage import Stage
from src.background import TiledBackground, StarsBackground

class Stage1(Stage):
    def __init__(self):
        super().__init__(TiledBackground(["grass_bg", "grass2_bg", "grass3_bg"]), "stage3music")
        # super().__init__(StarsBackground(), "stage3music")

        self.show_title_card("Spirits Forest")

        self.tl.add(1, lambda: self.spawn("fairy", lane=1))
        self.tl.add(1.5, lambda: self.spawn("fairy", lane=2))
        self.tl.add(2, lambda: self.spawn("fairy", lane=3))
        self.tl.add(2.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(3, lambda: self.spawn("fairy", lane=5))

        self.tl.add(5, lambda: self.spawn("fairy", lane=5))
        self.tl.add(5.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(6, lambda: self.spawn("fairy", lane=3))
        self.tl.add(6.5, lambda: self.spawn("fairy", lane=2))
        self.tl.add(7, lambda: self.spawn("fairy", lane=1))

        self.tl.add(10, lambda: self.spawn("fairy2", lane=1))
        self.tl.add(11, lambda: self.spawn("fairy2", lane=5))

        self.tl.add(13, lambda: self.spawn("fairy", lane=1))
        self.tl.add(13.5, lambda: self.spawn("fairy", lane=2))
        self.tl.add(14, lambda: self.spawn("fairy", lane=1))
        self.tl.add(14.5, lambda: self.spawn("fairy", lane=2))

        self.tl.add(16, lambda: self.spawn("fairy", lane=5))
        self.tl.add(16.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(17, lambda: self.spawn("fairy", lane=5))
        self.tl.add(17.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(18, lambda: self.spawn("fairy", lane=5))

        self.tl.add(20, lambda: self.spawn("fairy2", lane=3))
        self.tl.add(21, lambda: self.spawn("fairy2", lane=2))
        self.tl.add(22, lambda: self.spawn("fairy2", lane=1))

        self.tl.add(26, lambda: self.spawn_boss("boss1", lane=3))

        self.tl.add(30, lambda: self.spawn("fairy", lane=1))
        self.tl.add(31.5, lambda: self.spawn("fairy", lane=2))
        self.tl.add(32, lambda: self.spawn("fairy", lane=3))
        self.tl.add(32.5, lambda: self.spawn("fairy", lane=4))

        self.tl.add(34, lambda: self.spawn("fairy", lane=5))
        self.tl.add(34.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(35, lambda: self.spawn("fairy", lane=3))
        self.tl.add(35.5, lambda: self.spawn("fairy", lane=2))

        self.tl.add(37, lambda: self.spawn("fairy2", lane=5))
        self.tl.add(37.5, lambda: self.spawn("fairy2", lane=1))

        self.tl.add(38.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(39, lambda: self.spawn("fairy", lane=2))
        self.tl.add(39.5, lambda: self.spawn("fairy", lane=4))
        self.tl.add(40, lambda: self.spawn("fairy", lane=2))
