import random
from dataclasses import dataclass
from typing import List, Optional
from snake import Position


@dataclass
class Food:
    position: Position
    score_value: int = 10

    @staticmethod
    def create(
        grid_width: int = 20,
        grid_height: int = 20,
        snake_positions: Optional[List[Position]] = None,
    ) -> "Food":
        valid_positions = [
            Position(x, y)
            for x in range(grid_width)
            for y in range(grid_height)
        ]
        if snake_positions:
            valid_positions = [p for p in valid_positions if p not in snake_positions]

        if not valid_positions:
            return Food(position=Position(grid_width // 2, grid_height // 2))

        position = random.choice(valid_positions)
        return Food(position=position)

    def eat(self) -> int:
        return self.score_value

    def respawn(self, grid_width: int = 20, grid_height: int = 20, snake_positions: Optional[List[Position]] = None):
        valid_positions = [
            Position(x, y)
            for x in range(grid_width)
            for y in range(grid_height)
        ]
        if snake_positions:
            valid_positions = [p for p in valid_positions if p not in snake_positions]

        if valid_positions:
            self.position = random.choice(valid_positions)