from typing import TypedDict


class EnemyType(TypedDict):
    texture: str
    speed: float
    health: int
    emitter: str
    cooldown: float
    bonus_chance: int
    score: int


ENEMIES: dict[str, EnemyType] = {
    "fairy": {
        "texture": "blue_fairy",
        "speed": 200,
        "health": 3,
        "emitter": "single",
        "cooldown": 3,
        "bonus_chance": 50,
        "score": 30,
    },
    "fairy2": {
        "texture": "red_fairy",
        "speed": 150,
        "health": 7,
        "emitter": "shotgun",
        "cooldown": 2,
        "bonus_chance": 75,
        "score": 60,
    },
    "boss1": {
        "texture": "boss1",
        "speed": 200,
        "health": 80,
        "emitter": "",
        "cooldown": 0,
        "bonus_chance": 100,
        "score": 120,
    },


    "survival_fairy": {
        "texture": "blue_fairy",
        "speed": 160,
        "health": 2,
        "emitter": "fork",
        "cooldown": 3,
        "bonus_chance": 50,
        "score": 30,
    },
}
