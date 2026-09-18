import pyray as rl
import math
import random
from abc import ABC, abstractmethod
from src.constants import AREA_WIDTH, AREA_HEIGHT
from src.asset_store import AssetStore


class Background(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass


class ScrollingBackground(Background):
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


class StarsBackground(Background):
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


class TiledBackground(Background):
    def __init__(self, textures: list[str]):
        self.textures = [AssetStore.get(t) for t in textures]
        self.texture_scale = 4
        self.speed = 80
        self.x_count = math.ceil(AREA_WIDTH / self.textures[0].width * self.texture_scale)
        self.y_count = math.ceil(AREA_HEIGHT / self.textures[0].height * self.texture_scale) + 1
        self.tiles = []

        for col in range(self.x_count):
            for row in range(self.y_count):
                x = col * self.textures[0].width * self.texture_scale
                y = (row - 1) * self.textures[0].height * self.texture_scale
                texture = random.choice(self.textures)
                self.tiles.append((x, y, texture))

    def update(self, dt: float):
        for i, (x, y, texture) in enumerate(self.tiles):
            y += self.speed * dt

            if y >= AREA_HEIGHT:
                y -= (self.y_count - 1) * self.textures[0].height * self.texture_scale

            self.tiles[i] = (x, y, texture)

    def draw(self):
        for (x, y, texture) in self.tiles:
            rl.draw_texture_ex(texture, (x, y), 0, self.texture_scale, rl.GRAY)
