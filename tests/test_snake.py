import pytest
from snake import Snake, Direction, Position


def test_snake_spawns_within_grid():
    """Snake should spawn at a random position within the grid bounds."""
    snake = Snake(grid_width=30, grid_height=25)

    assert len(snake.positions) == 3
    for pos in snake.positions:
        assert 0 <= pos.x < 30, f"x={pos.x} out of bounds [0, 30)"
        assert 0 <= pos.y < 25, f"y={pos.y} out of bounds [0, 25)"
    head = snake.positions[0]
    assert abs(snake.positions[1].x - head.x) + abs(snake.positions[1].y - head.y) == 1
    assert abs(snake.positions[2].x - snake.positions[1].x) + abs(snake.positions[2].y - snake.positions[1].y) == 1


def test_snake_initial_direction():
    snake = Snake()
    assert snake.direction == Direction.RIGHT


def test_snake_move_forward():
    snake = Snake()
    snake.direction = Direction.RIGHT
    initial_x = snake.positions[0].x
    snake.move()

    head = snake.positions[0]
    assert head.x == initial_x + 1


def test_snake_change_direction():
    snake = Snake()
    snake.change_direction(Direction.UP)
    snake.move()
    assert snake.direction == Direction.UP


def test_snake_cannot_reverse():
    snake = Snake()
    snake.direction = Direction.RIGHT
    snake.change_direction(Direction.LEFT)
    snake.move()
    assert snake.direction == Direction.RIGHT

    snake.change_direction(Direction.DOWN)
    snake.move()
    assert snake.direction == Direction.DOWN


def test_snake_queued_direction_applied():
    snake = Snake()
    snake.direction = Direction.RIGHT

    snake.change_direction(Direction.DOWN)
    snake.move()
    assert snake.direction == Direction.DOWN

    snake.change_direction(Direction.LEFT)
    snake.move()
    assert snake.direction == Direction.LEFT


def test_snake_change_to_same_is_ok():
    snake = Snake()
    snake.direction = Direction.UP
    snake.change_direction(Direction.UP)
    assert snake.direction == Direction.UP