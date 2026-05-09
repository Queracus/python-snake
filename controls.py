from enum import Enum, auto
from snake import Direction


class ControlScheme(Enum):
    ARROWS = auto()
    WASD = auto()


def map_key_to_direction(key: str, scheme: ControlScheme) -> Direction | None:
    if scheme == ControlScheme.ARROWS:
        arrows = {
            "Up": Direction.UP,
            "Down": Direction.DOWN,
            "Left": Direction.LEFT,
            "Right": Direction.RIGHT,
        }
        return arrows.get(key)
    elif scheme == ControlScheme.WASD:
        wasd = {
            "w": Direction.UP,
            "s": Direction.DOWN,
            "a": Direction.LEFT,
            "d": Direction.RIGHT,
        }
        return wasd.get(key.lower())
    return None