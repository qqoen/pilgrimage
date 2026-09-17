import pyray as rl
import math
import random
from src.constants import AREA_WIDTH, AREA_HEIGHT


class ScrollingBackground:
    def __init__(self, texture):
        self.texture = texture
        self.speed = 50
        self.parts = [(0, 0), (0, -self.texture.height * 2)]

    def update(self, dt):
        for i, (x, y) in enumerate(self.parts):
            dy = y + self.speed * dt

            if dy >= AREA_HEIGHT:
                dy -= self.texture.height * 2 * 2

            self.parts[i] = (x, dy)

    def draw(self):
        for (x, y) in self.parts:
            rl.draw_texture_ex(self.texture, (x, y), 0, 2, rl.GRAY)


class StarsBackground:
    def __init__(self):
        self.stars = []

        for i in range(100):
            x = random.randint(0, AREA_WIDTH - 1)
            y = random.randint(0, AREA_HEIGHT - 1)
            spd = random.randint(100, 200)

            self.stars.append((x, y, spd))

    def update(self, dt):
        for i, (x, y, spd) in enumerate(self.stars):
            y += spd * dt

            if y >= AREA_HEIGHT:
                y -= AREA_HEIGHT

            self.stars[i] = (x, y, spd)

    def draw(self):
        for i, (x, y, spd) in enumerate(self.stars):
            rl.draw_rectangle(x, int(y), 4, 4, rl.WHITE if spd > 150 else rl.GRAY)


class TiledBackground:
    def __init__(self, texture):
        self.texture = texture
        self.texture_scale = 4

        self.x_count = math.ceil(AREA_WIDTH / self.texture.width * self.texture_scale)
        self.y_count = math.ceil(AREA_HEIGHT / self.texture.height * self.texture_scale) + 1

        self.tiles = []
        self.speed = 40

        for col in range(self.x_count):
            for row in range(self.y_count):
                x = col * self.texture.width * self.texture_scale
                y = (row - 1) * self.texture.height * self.texture_scale
                self.tiles.append((x, y))

        (_, self.max_y) = self.tiles[-1]

    def update(self, dt: float):
        miny = -self.texture.height

        for i, (x, y) in enumerate(self.tiles):
            miny = min(miny, y)
            dy = y + self.speed * dt

            if dy >= AREA_HEIGHT:
                dy -= self.max_y

            self.tiles[i] = (x, dy)

    def draw(self):
        for (x, y) in self.tiles:
            rl.draw_texture_ex(self.texture, (x, y), 0, self.texture_scale, rl.GRAY)
