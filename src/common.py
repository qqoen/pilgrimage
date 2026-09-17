import pyray as rl
import random


def update_list(objects, dt):
    for obj in objects:
        obj.update(dt)
        if obj.is_destroyed:
            objects.remove(obj)


def draw_list(objects):
    for obj in objects:
        obj.draw()


def approach(val, target, speed):
    diff = val - target
    val += -sign(diff) * (abs(diff) // 2) * speed

    snap_threshold = 4

    if abs(val - target) <= snap_threshold:
        val = target

    return val


def sign(val):
    if val < 0:
        return -1
    if val > 0:
        return 1
    return 0


def play_sound(sound: rl.Sound):
    rl.set_sound_pitch(sound, random.uniform(0.8, 1.2))
    rl.play_sound(sound)
