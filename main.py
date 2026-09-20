import pyray as rl
import raylib
from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, FPS, IS_DEBUG
from src.game import Game
from src.common import *
from src.asset_store import AssetStore


def main():
    rl.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Pilgrimage")
    rl.init_audio_device()

    rl.set_target_fps(FPS)
    rl.set_exit_key(raylib.KEY_DELETE if IS_DEBUG else raylib.KEY_NULL)
    rl.hide_cursor()

    load_assets()

    game = Game()

    should_exit = lambda: rl.window_should_close() or game.player_data.should_quit

    while not should_exit():
        dt = rl.get_frame_time()
        game.update(dt)
        rl.begin_drawing()
        game.draw()
        rl.end_drawing()

    rl.close_audio_device()
    rl.close_window()


def load_assets():
    AssetStore.load_texture("player1", "new_player1.png")
    AssetStore.load_texture("player2", "new_player1.png")
    AssetStore.load_texture("player3", "new_player1.png")
    AssetStore.load_texture("player4", "new_player1.png")

    AssetStore.load_texture("mushroom", "mushroom.png")
    AssetStore.load_texture("mushroom2", "mushroom2.png")
    AssetStore.load_texture("boss1", "boss1.png")

    AssetStore.load_texture("grass_bg", "bluegrass1.png")
    AssetStore.load_texture("grass2_bg", "bluegrass2.png")
    AssetStore.load_texture("grass3_bg", "bluegrass3.png")

    AssetStore.load_texture("spell", "spell_lowres.png")

    AssetStore.load_texture("bullet", "spore_bullet.png")
    AssetStore.load_texture("player_bullet", "flower_bullet.png")
    AssetStore.load_texture("bonus", "bonus.png")

    AssetStore.load_music("stage2music", "05. Long Journey.ogg")
    AssetStore.load_music("stage3music", "07. Spirits Forest (full).ogg")

    AssetStore.load_sound("shoot_sound", "Hit.wav")
    AssetStore.load_sound("hit_sound", "Hit2.wav")
    AssetStore.load_sound("destroy_sound", "Boom7.wav")
    AssetStore.load_sound("pickup", "Pickup11.wav")
    AssetStore.load_sound("enemy_shot", "enemy_shot.wav")

    AssetStore.load_font("font", "Chewy-Regular.ttf")


main()
