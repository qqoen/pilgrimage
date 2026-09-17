import pyray as rl


class Sprite:
    def __init__(self, texture: rl.Texture, texture_scale=1, tint=rl.WHITE):
        self.texture = texture
        self.texture_scale = texture_scale
        self.tint = tint

    @property
    def width(self):
        return self.texture.width * self.texture_scale

    @property
    def height(self):
        return self.texture.height * self.texture_scale

    def draw(self, x, y):
        x = x - self.width // 2
        y = y - self.height // 2
        rl.draw_texture_ex(self.texture, (x, y), 0, self.texture_scale, self.tint)
