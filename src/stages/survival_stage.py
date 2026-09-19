from .stage import Stage
from src.background import TiledBackground
from src.common import Timer
from src.data import ENEMIES, EnemyType
import random


class SurvivalStage(Stage):
    def __init__(self):
        super().__init__(TiledBackground(["grass_bg", "grass2_bg", "grass3_bg"]), "stage2music", "Survival")

        self.spawn_timer = Timer(2, True)
        self.rank_timer = Timer(5, True)
        self.rank = 0

    def update(self, dt):
        super().update(dt)

        self.spawn_timer.update(dt)
        self.rank_timer.update(dt)

        if self.spawn_timer.finished:
            lane = random.randint(1, 5)
            self.spawn("survival_fairy", lane)
            self.spawn_timer.start()

        if self.rank_timer.finished:
            if self.rank <= 7:
                self.rank += 1
                self.spawn_timer = Timer(2 - self.rank * 0.2, True)
                self.rank_timer.start()
