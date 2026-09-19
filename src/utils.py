import pyray as rl
import random
from src.constants import WINDOW_WIDTH


def update_list(objects, dt):
    for obj in objects:
        obj.update(dt)
        if obj.is_destroyed:
            objects.remove(obj)


def draw_list(objects):
    for obj in objects:
        obj.draw()


def play_sound(sound: rl.Sound):
    rl.set_sound_pitch(sound, random.uniform(0.8, 1.2))
    rl.play_sound(sound)


def print_center(font: rl.Font, text: str, font_size: int, y: int, color=rl.WHITE, area_width=WINDOW_WIDTH):
    width = rl.measure_text_ex(font, text, font_size, 3)
    rl.draw_text_ex(font, text, (area_width // 2 - width.x // 2, y), font_size, 3, color)
