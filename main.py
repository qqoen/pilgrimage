import pyray as rl
import raylib
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH
from src.game import Game
from src.common import *
from src.asset_store import AssetStore


def main():
    rl.set_target_fps(60)
    rl.set_exit_key(raylib.KEY_ESCAPE)
    rl.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Pilgrimage")
    rl.init_audio_device()

    AssetStore.load_texture("player_texture", "witch.png")
    AssetStore.load_texture("bg1_texture", "tile1.png")
    AssetStore.load_texture("enemy1_texture", "enemy2.png")
    AssetStore.load_texture("bullet", "red_bullet.png")
    AssetStore.load_texture("player_bullet", "plr_bullet.png")
    AssetStore.load_texture("bonus", "bonus.png")
    # AssetStore.load_texture("bg2_texture", "Blue_Nebula_02-512x512.png")
    AssetStore.load_texture("bg2_texture", "Puffy_Sky-Night_01-512x512.png")

    song_name = "07. Spirits Forest (full).ogg"
    AssetStore.load_music("music", song_name)

    AssetStore.load_sound("shoot_sound", "Hit.wav")
    AssetStore.load_sound("hit_sound", "Hit2.wav")
    AssetStore.load_sound("destroy_sound", "Boom7.wav")
    AssetStore.load_sound("pickup", "Pickup11.wav")

    font = rl.load_font("assets/Chewy-Regular.ttf")
    AssetStore._assets["font"] = font

    game = Game(song_name)

    while not rl.window_should_close():
        dt = rl.get_frame_time()
        game.update(dt)
        rl.begin_drawing()
        game.draw()
        rl.end_drawing()

    AssetStore.unload()

    rl.close_audio_device()
    rl.close_window()

main()
