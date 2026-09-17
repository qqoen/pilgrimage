from typing import TypedDict


class EnemyType(TypedDict):
    texture: str
    speed: float
    health: int
    emitter: str


ENEMIES: dict[str, EnemyType] = {
    "fairy": {
        "texture": "enemy1_texture",
        "speed": 200,
        "health": 3,
        "emitter": "fork",
    },
}
