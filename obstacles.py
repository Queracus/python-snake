import random
from dataclasses import dataclass
from typing import List, Optional
from snake import Position


@dataclass
class Obstacles:
    positions: List[Position]

    @staticmethod
    def create(
        grid_width: int = 20,
        grid_height: int = 20,
        count: int = 0,
        snake_positions: Optional[List[Position]] = None,
    ) -> "Obstacles":
        valid_positions = [
            Position(x, y)
            for x in range(grid_width)
            for y in range(grid_height)
        ]

        if snake_positions:
            valid_positions = [p for p in valid_positions if p not in snake_positions]

        start_positions = [
            Position(grid_width // 2, grid_height // 2),
            Position(grid_width // 2 - 1, grid_height // 2),
            Position(grid_width // 2 - 2, grid_height // 2),
        ]
        valid_positions = [p for p in valid_positions if p not in start_positions]

        if count > len(valid_positions):
            count = len(valid_positions)

        positions = random.sample(valid_positions, count)
        return Obstacles(positions=positions)

    def check_collision(self, head: Position) -> bool:
        return head in self.positions