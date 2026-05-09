import pytest
from snake import Snake, Position
from obstacles import Obstacles


def test_obstacles_created_per_level():
    obstacles = Obstacles.create(grid_width=20, grid_height=20, count=5)
    assert len(obstacles.positions) == 5


def test_obstacles_not_on_snake():
    snake = Snake(grid_width=20, grid_height=20)
    obstacles = Obstacles.create(
        grid_width=20,
        grid_height=20,
        count=5,
        snake_positions=snake.positions
    )

    for obs in obstacles.positions:
        assert obs not in snake.positions


def test_obstacle_collision():
    obstacles = Obstacles.create(grid_width=20, grid_height=20, count=3)
    hit_position = obstacles.positions[0]
    head = Position(x=hit_position.x, y=hit_position.y)

    assert obstacles.check_collision(head) is True


def test_no_obstacle_collision():
    obstacles = Obstacles.create(grid_width=20, grid_height=20, count=3)

    head = Position(0, 0)

    assert obstacles.check_collision(head) is False


def test_obstacle_count_can_vary_by_level():
    obs1 = Obstacles.create(grid_width=20, grid_height=20, count=0)
    obs2 = Obstacles.create(grid_width=20, grid_height=20, count=10)
    obs3 = Obstacles.create(grid_width=20, grid_height=20, count=18)

    assert len(obs1.positions) == 0
    assert len(obs2.positions) == 10
    assert len(obs3.positions) == 18