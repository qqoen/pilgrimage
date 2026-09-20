import pyray as rl
from abc import ABC, abstractmethod
from src.asset_store import AssetStore


class Graphics(ABC):
    def __init__(self, tint):
        self.tint = tint

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, x, y):
        pass


class AnimatedSprite(Graphics):
    def __init__(self, frames: list[str], frame_duration: float, texture_scale=1, tint=rl.WHITE):
        super().__init__(tint)
        self.frames = [AssetStore.get(frame) for frame in frames]
        self.frame_duration = frame_duration
        self.texture_scale = texture_scale
        self.frame_idx = 0
        self.timer = self.frame_duration

    def width(self):
        return self.frames[0].width * self.texture_scale

    def height(self):
        return self.frames[0].height * self.texture_scale

    def update(self, dt):
        self.timer -= dt

        if self.timer <= 0:
            self.frame_idx += 1
            self.timer = self.frame_duration

        if self.frame_idx >= len(self.frames):
            self.frame_idx = 0

    def draw(self, x, y):
        x = x - self.width() // 2
        y = y - self.height() // 2
        rl.draw_texture_ex(self.frames[self.frame_idx], (x, y), 0, self.texture_scale, self.tint)


class Sprite(Graphics):
    def __init__(self, texture: rl.Texture, texture_scale=1, tint=rl.WHITE):
        super().__init__(tint)
        self.texture = texture
        self.texture_scale = texture_scale

    def width(self):
        return self.texture.width * self.texture_scale

    def height(self):
        return self.texture.height * self.texture_scale

    def update(self, dt):
        pass

    def draw(self, x, y):
        x = x - self.width() // 2
        y = y - self.height() // 2
        rl.draw_texture_ex(self.texture, (x, y), 0, self.texture_scale, self.tint)


class Shadow:
    def __init__(self, texture, texture_scale):
        self.sprite = Sprite(AssetStore.get(texture), texture_scale, rl.fade(rl.BLACK, 0.25))
        self.position = rl.Vector2()

    def update(self, dt, target):
        self.position.x = target.x
        self.position.y = target.y + 30

    def draw(self):
        self.sprite.draw(self.position.x, self.position.y)
