import pyray as rl
import os


class AssetStore:
    _assets = {}

    @staticmethod
    def load_texture(key, file_name):
        texture = rl.load_texture(os.path.join("assets", file_name))
        AssetStore._assets[key] = texture

    @staticmethod
    def load_music(key, file_name):
        music = rl.load_music_stream(os.path.join("assets", "audio", file_name))
        AssetStore._assets[key] = music

    @staticmethod
    def load_sound(key, file_name):
        sound = rl.load_sound(os.path.join("assets", "audio", file_name))
        AssetStore._assets[key] = sound

    @staticmethod
    def load_font(key, file_name):
        font = rl.load_font(os.path.join("assets", file_name))
        AssetStore._assets[key] = font

    @staticmethod
    def get(key):
        return AssetStore._assets[key]
