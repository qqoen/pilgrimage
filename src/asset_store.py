import pyray as rl
import os


class AssetStore:
    _assets = {}
    _music_stream_keys = []
    _sound_keys = []
    _texture_keys = []

    @staticmethod
    def load_texture(key, file_name):
        texture = rl.load_texture(os.path.join("assets", file_name))
        AssetStore._assets[key] = texture
        AssetStore._texture_keys.append(key)

    @staticmethod
    def load_music(key, file_name):
        music = rl.load_music_stream(os.path.join("assets", file_name))
        AssetStore._assets[key] = music
        AssetStore._music_stream_keys.append(key)

    @staticmethod
    def load_sound(key, file_name):
        sound = rl.load_sound(os.path.join("assets", file_name))
        AssetStore._assets[key] = sound
        AssetStore._sound_keys.append(key)

    @staticmethod
    def get(key):
        return AssetStore._assets[key]

    @staticmethod
    def unload():
        for key in AssetStore._music_stream_keys:
            rl.unload_music_stream(AssetStore.get(key))
        for key in AssetStore._sound_keys:
            rl.unload_sound(AssetStore.get(key))
        for key in AssetStore._texture_keys:
            rl.unload_texture(AssetStore.get(key))

