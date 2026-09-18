from typing import TypedDict


class EnemyType(TypedDict):
    texture: str
    speed: float
    health: int
    emitter: str
    cooldown: float


ENEMIES: dict[str, EnemyType] = {
    "fairy": {
        "texture": "blue_fairy",
        "speed": 200,
        "health": 3,
        "emitter": "single",
        "cooldown": 3,
    },
    "fairy2": {
        "texture": "red_fairy",
        "speed": 200,
        "health": 7,
        "emitter": "shotgun",
        "cooldown": 1.5,
    },
    "boss1": {
        "texture": "boss1",
        "speed": 200,
        "health": 80,
        "emitter": "",
        "cooldown": 0,
    },
}
