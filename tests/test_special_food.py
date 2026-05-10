import pytest
from snake import Snake, Position
from food import SpecialFood


def test_special_food_spawns_on_grid():
    sf = SpecialFood.create(grid_width=20, grid_height=20)
    assert 0 <= sf.position.x < 20
    assert 0 <= sf.position.y < 20


def test_special_food_does_not_spawn_on_snake():
    snake = Snake(grid_width=20, grid_height=20)
    sf = SpecialFood.create(grid_width=20, grid_height=20, snake_positions=snake.positions)

    assert sf.position not in snake.positions


def test_special_food_does_not_spawn_on_normal_food():
    from food import Food
    snake = Snake(grid_width=20, grid_height=20)
    food = Food.create(grid_width=20, grid_height=20, snake_positions=snake.positions)
    sf = SpecialFood.create(
        grid_width=20,
        grid_height=20,
        snake_positions=snake.positions,
        food_position=food.position
    )

    assert sf.position != food.position


def test_special_food_eat_returns_30():
    sf = SpecialFood.create(grid_width=20, grid_height=20)
    assert sf.eat() == 30


def test_special_food_tick_countdown():
    sf = SpecialFood.create(grid_width=20, grid_height=20, tick_rate=150)
    initial_ticks = sf.remaining_ticks

    assert sf.tick() is True
    assert sf.remaining_ticks == initial_ticks - 1


def test_special_food_expires():
    sf = SpecialFood(position=Position(5, 5), remaining_ticks=1)

    assert sf.tick() is False