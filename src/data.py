from typing import TypedDict


class EnemyType(TypedDict):
    texture: str
    speed: float
    health: int
    emitter: str


ENEMIES: dict[str, EnemyType] = {
    "fairy": {
        "texture": "blue_fairy",
        "speed": 200,
        "health": 3,
        "emitter": "fork",
    },
    "fairy2": {
        "texture": "red_fairy",
        "speed": 200,
        "health": 6,
        "emitter": "shotgun",
    },
    "fairy3": {
        "texture": "green_fairy",
        "speed": 200,
        "health": 3,
        "emitter": "fork",
    },
}
