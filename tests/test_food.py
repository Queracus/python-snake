import pytest
from snake import Snake, Position
from food import Food


def test_food_spawns_on_grid():
    food = Food.create(grid_width=20, grid_height=20)
    assert 0 <= food.position.x < 20
    assert 0 <= food.position.y < 20


def test_food_does_not_spawn_on_snake():
    snake = Snake(grid_width=20, grid_height=20)
    food = Food.create(grid_width=20, grid_height=20, snake_positions=snake.positions)

    assert food.position not in snake.positions


def test_food_eaten_increases_score():
    food = Food.create(grid_width=20, grid_height=20)
    score = food.eat()
    assert score == 10


def test_food_respawns_not_on_snake():
    snake = Snake(grid_width=20, grid_height=20)
    food = Food.create(grid_width=20, grid_height=20, snake_positions=snake.positions)

    old_pos = food.position
    food.respawn(grid_width=20, grid_height=20, snake_positions=snake.positions)

    assert food.position != old_pos
    assert food.position not in snake.positions