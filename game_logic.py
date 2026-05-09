from typing import List
from snake import Position


def check_wall_collision(head: Position, grid_width: int, grid_height: int) -> bool:
    return head.x < 0 or head.x >= grid_width or head.y < 0 or head.y >= grid_height


def check_self_collision(positions: List[Position]) -> bool:
    if len(positions) < 3:
        return False
    head = positions[0]
    return head in positions[1:]


def check_food_collision(head: Position, food_position: Position) -> bool:
    return head.x == food_position.x and head.y == food_position.y