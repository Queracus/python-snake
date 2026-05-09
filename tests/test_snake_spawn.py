import pytest
from snake import Snake, Position
from game_logic import check_self_collision, check_wall_collision


def test_snake_no_self_collision_after_one_move():
    """Snake should not collide with itself immediately after spawning and moving."""
    for _ in range(100):
        snake = Snake(grid_width=20, grid_height=20)
        snake.move()
        assert not check_self_collision(snake.positions), \
            f"Self collision after move with positions {[(p.x,p.y) for p in snake.positions]}"


def test_snake_stays_in_bounds_after_one_move():
    """Snake head should stay within grid bounds after one move."""
    for _ in range(100):
        snake = Snake(grid_width=20, grid_height=20)
        initial_head = snake.positions[0]
        snake.move()
        head = snake.positions[0]
        assert 0 <= head.x < snake.grid_width, \
            f"x={head.x} out of bounds [0, {snake.grid_width})"
        assert 0 <= head.y < snake.grid_height, \
            f"y={head.y} out of bounds [0, {snake.grid_height})"