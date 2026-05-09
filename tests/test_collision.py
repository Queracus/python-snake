import pytest
from snake import Snake, Position
from food import Food
from game_logic import check_wall_collision, check_self_collision, check_food_collision


def test_wall_collision_on_right():
    snake = Snake(grid_width=20, grid_height=20)
    snake.positions[0] = Position(20, 10)

    assert check_wall_collision(snake.positions[0], 20, 20) is True


def test_wall_collision_on_left():
    snake = Snake(grid_width=20, grid_height=20)
    snake.positions[0] = Position(-1, 10)

    assert check_wall_collision(snake.positions[0], 20, 20) is True


def test_wall_collision_on_top():
    snake = Snake(grid_width=20, grid_height=20)
    snake.positions[0] = Position(10, -1)

    assert check_wall_collision(snake.positions[0], 20, 20) is True


def test_wall_collision_on_bottom():
    snake = Snake(grid_width=20, grid_height=20)
    snake.positions[0] = Position(10, 20)

    assert check_wall_collision(snake.positions[0], 20, 20) is True


def test_no_wall_collision():
    snake = Snake(grid_width=20, grid_height=20)

    assert check_wall_collision(snake.positions[0], 20, 20) is False


def test_self_collision():
    snake = Snake(grid_width=20, grid_height=20)
    snake.positions = [
        Position(10, 10),
        Position(10, 9),
        Position(10, 10),
    ]

    assert check_self_collision(snake.positions) is True


def test_no_self_collision():
    snake = Snake(grid_width=20, grid_height=20)

    assert check_self_collision(snake.positions) is False


def test_food_collision():
    snake = Snake(grid_width=20, grid_height=20)
    food = Food.create(grid_width=20, grid_height=20)
    food.position = snake.positions[0]

    assert check_food_collision(snake.positions[0], food.position) is True


def test_no_food_collision():
    snake = Snake(grid_width=20, grid_height=20)
    food = Food.create(grid_width=20, grid_height=20)

    assert check_food_collision(snake.positions[0], food.position) is False