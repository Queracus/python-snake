import pytest
from snake import Direction
from enum import Enum, auto


class ControlScheme(Enum):
    ARROWS = auto()
    WASD = auto()


def test_arrow_keys_map_to_direction():
    from controls import map_key_to_direction, ControlScheme

    assert map_key_to_direction("Up", ControlScheme.ARROWS) == Direction.UP
    assert map_key_to_direction("Down", ControlScheme.ARROWS) == Direction.DOWN
    assert map_key_to_direction("Left", ControlScheme.ARROWS) == Direction.LEFT
    assert map_key_to_direction("Right", ControlScheme.ARROWS) == Direction.RIGHT


def test_wasd_map_to_direction():
    from controls import map_key_to_direction, ControlScheme

    assert map_key_to_direction("w", ControlScheme.WASD) == Direction.UP
    assert map_key_to_direction("s", ControlScheme.WASD) == Direction.DOWN
    assert map_key_to_direction("a", ControlScheme.WASD) == Direction.LEFT
    assert map_key_to_direction("d", ControlScheme.WASD) == Direction.RIGHT


def test_invalid_key_returns_none():
    from controls import map_key_to_direction, ControlScheme

    assert map_key_to_direction("x", ControlScheme.ARROWS) is None
    assert map_key_to_direction("q", ControlScheme.WASD) is None