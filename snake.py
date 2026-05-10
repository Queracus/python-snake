from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum, auto
import random


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
        self.pending_direction: Direction | None = None
        self.positions: List[Position] = []
        self._reset()

    def _reset(self):
        min_start = 7
        max_start_x = self.grid_width - 8
        max_start_y = self.grid_height - 8
        start_x = random.randint(min_start, max_start_x)
        start_y = random.randint(min_start, max_start_y)
        self.positions = [
            Position(start_x, start_y),
            Position(start_x - 1, start_y),
            Position(start_x - 2, start_y),
        ]
        self.direction = Direction.RIGHT
        self.pending_direction = None

    def move(self):
        # Apply pending direction if any (only one change per tick)
        if self.pending_direction:
            if self._is_valid_direction(self.pending_direction):
                self.direction = self.pending_direction
            self.pending_direction = None

        head = self.positions[0]
        dx, dy = self._direction_delta()
        new_head = Position(head.x + dx, head.y + dy)
        self.positions.insert(0, new_head)
        self.positions.pop()

    def _is_valid_direction(self, new_direction: Direction) -> bool:
        reverses = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return new_direction != reverses.get(self.direction)

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
        # Queue direction change - will be applied on next move
        if self._is_valid_direction(new_direction):
            self.pending_direction = new_direction