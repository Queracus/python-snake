import pytest
from snake import Snake, Direction, Position


def test_snake_initial_position():
    snake = Snake(grid_width=20, grid_height=20)
    cx, cy = 10, 10

    assert len(snake.positions) == 3
    assert snake.positions[0] == Position(cx, cy)
    assert snake.positions[1] == Position(cx - 1, cy)
    assert snake.positions[2] == Position(cx - 2, cy)


def test_snake_initial_direction():
    snake = Snake()
    assert snake.direction == Direction.RIGHT


def test_snake_move_forward():
    snake = Snake()
    snake.move()

    head = snake.positions[0]
    assert head.x == 11


def test_snake_change_direction():
    snake = Snake()
    snake.change_direction(Direction.UP)
    assert snake.direction == Direction.UP


def test_snake_cannot_reverse():
    snake = Snake()
    snake.direction = Direction.RIGHT
    snake.change_direction(Direction.LEFT)
    assert snake.direction == Direction.RIGHT

    snake.change_direction(Direction.DOWN)
    assert snake.direction == Direction.DOWN


def test_snake_change_to_same_is_ok():
    snake = Snake()
    snake.direction = Direction.UP
    snake.change_direction(Direction.UP)
    assert snake.direction == Direction.UP