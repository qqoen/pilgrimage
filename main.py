import pyray as rl
import raylib
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, FPS
from src.game import Game
from src.common import *
from src.asset_store import AssetStore


def main():
    rl.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Pilgrimage")
    rl.init_audio_device()

    rl.set_target_fps(FPS)
    rl.set_exit_key(raylib.KEY_DELETE)
    rl.hide_cursor()

    load_assets()

    game = Game()

    while not rl.window_should_close():
        dt = rl.get_frame_time()
        game.update(dt)
        rl.begin_drawing()
        game.draw()
        rl.end_drawing()

    rl.close_audio_device()
    rl.close_window()


def load_assets():
    AssetStore.load_texture("player1", "player1.png")
    AssetStore.load_texture("player2", "player2.png")
    AssetStore.load_texture("player3", "player3.png")
    AssetStore.load_texture("player4", "player4.png")

    AssetStore.load_texture("blue_fairy", "blue_fairy.png")
    AssetStore.load_texture("red_fairy", "red_fairy.png")
    AssetStore.load_texture("green_fairy", "green_fairy.png")
    AssetStore.load_texture("boss1", "boss1.png")

    AssetStore.load_texture("checkers_bg", "tile1.png")
    AssetStore.load_texture("mossy_bg", "mossy.png")
    AssetStore.load_texture("grass_bg", "grass.png")
    AssetStore.load_texture("grass2_bg", "grass2.png")
    AssetStore.load_texture("grass3_bg", "grass3.png")
    AssetStore.load_texture("stage2bg", "stage2.png")
    AssetStore.load_texture("stage3bg", "Puffy_Sky-Night_01-512x512.png")

    AssetStore.load_texture("bullet", "red_bullet.png")
    AssetStore.load_texture("player_bullet", "plr_bullet.png")
    AssetStore.load_texture("bonus", "bonus.png")

    AssetStore.load_music("stage2music", "05. Long Journey.ogg")
    AssetStore.load_music("stage3music", "07. Spirits Forest (full).ogg")

    AssetStore.load_sound("shoot_sound", "Hit.wav")
    AssetStore.load_sound("hit_sound", "Hit2.wav")
    AssetStore.load_sound("destroy_sound", "Boom7.wav")
    AssetStore.load_sound("pickup", "Pickup11.wav")

    AssetStore.load_font("font", "Chewy-Regular.ttf")


main()
