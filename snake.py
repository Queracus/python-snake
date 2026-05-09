from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum, auto


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Position:
    x: int
    y: int


class Snake:
    def __init__(self, grid_width: int = 20, grid_height: int = 20):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.direction = Direction.RIGHT
        self.positions: List[Position] = []
        self._reset()

    def _reset(self):
        cx, cy = self.grid_width // 2, self.grid_height // 2
        self.positions = [
            Position(cx, cy),
            Position(cx - 1, cy),
            Position(cx - 2, cy),
        ]
        self.direction = Direction.RIGHT

    def move(self):
        head = self.positions[0]
        dx, dy = self._direction_delta()
        new_head = Position(head.x + dx, head.y + dy)
        self.positions.insert(0, new_head)
        self.positions.pop()

    def _direction_delta(self) -> Tuple[int, int]:
        if self.direction == Direction.UP:
            return (0, -1)
        elif self.direction == Direction.DOWN:
            return (0, 1)
        elif self.direction == Direction.LEFT:
            return (-1, 0)
        elif self.direction == Direction.RIGHT:
            return (1, 0)
        return (1, 0)

    def change_direction(self, new_direction: Direction):
        reverses = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        if new_direction != reverses.get(self.direction):
            self.direction = new_direction