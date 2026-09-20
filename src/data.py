from typing import TypedDict


class EnemyType(TypedDict):
    texture: str
    speed: float
    health: int
    emitter: str
    cooldown: float
    bonus_chance: int
    bonus_count: int
    score: int
    behavior: str


ENEMIES: dict[str, EnemyType] = {
    "fairy": {
        "texture": "mushroom",
        "speed": 200,
        "health": 3,
        "emitter": "single",
        "cooldown": 3,
        "bonus_chance": 50,
        "bonus_count": 3,
        "score": 30,
        "behavior": "move",
    },

    "mushroom2": {
        "texture": "mushroom",
        "speed": 150,
        "health": 3,
        "emitter": "single_aimed",
        "cooldown": 3,
        "bonus_chance": 50,
        "bonus_count": 3,
        "score": 40,
        "behavior": "",
    },

    "fairy2": {
        "texture": "mushroom2",
        "speed": 150,
        "health": 7,
        "emitter": "shotgun",
        "cooldown": 2,
        "bonus_chance": 75,
        "bonus_count": 4,
        "score": 60,
        "behavior": "",
    },

    "red_mushroom2": {
        "texture": "mushroom2",
        "speed": 150,
        "health": 7,
        "emitter": "circle",
        "cooldown": 2,
        "bonus_chance": 75,
        "bonus_count": 4,
        "score": 60,
        "behavior": "",
    },


    "boss1": {
        "texture": "boss1",
        "speed": 275,
        "health": 80,
        "emitter": "",
        "cooldown": 0,
        "bonus_chance": 100,
        "bonus_count": 6,
        "score": 120,
        "behavior": "",
    },

    "survival_fairy": {
        "texture": "mushroom",
        "speed": 160,
        "health": 2,
        "emitter": "fork",
        "cooldown": 3,
        "bonus_chance": 50,
        "bonus_count": 3,
        "score": 30,
        "behavior": "",
    },
}
