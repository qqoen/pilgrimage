import pyray as rl
import random
from src.utils import update_list, draw_list


class Blast:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.radius = 0.0
        self.max_radius = 32.0
        self.is_destroyed = False
        self.color = random.choice([rl.WHITE, rl.SKYBLUE, rl.BLUE])
        self.offset = random.randint(0, 3)

    def update(self, dt):
        if self.offset > 0:
            self.offset -= dt * 20
            return

        self.radius += 200 * dt
        if self.radius > self.max_radius:
            self.is_destroyed = True

    def draw(self):
        rl.draw_circle(self.x, self.y, int(self.radius), self.color)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blast_count = random.randint(1, 3)
        self.blasts = []

        for _ in range(self.blast_count):
            x = self.x + random.randint(-15, 15)
            y = self.y + random.randint(-15, 15)
            self.blasts.append(Blast(x, y))

        self.is_destroyed = False

    def update(self, dt):
        update_list(self.blasts, dt)

        if len(self.blasts) == 0:
            self.is_destroyed = True

    def draw(self):
        draw_list(self.blasts)
