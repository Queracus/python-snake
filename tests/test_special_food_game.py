import pytest
from game import Game, GameState
from snake import Snake, Position
from food import Food, SpecialFood


@pytest.fixture
def game_fixture():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1)
    yield game
    root.destroy()


def test_special_food_spawns_after_interval(game_fixture):
    game = game_fixture
    game.special_food_spawn_timer = 10000

    initial_count = len(game.special_foods)
    game.handle_special_food()

    assert len(game.special_foods) > initial_count


def test_special_food_max_2_on_board(game_fixture):
    game = game_fixture
    game.special_foods = [
        SpecialFood(position=Position(1, 1), remaining_ticks=10),
        SpecialFood(position=Position(2, 2), remaining_ticks=10),
    ]
    game.special_food_spawn_timer = 10000

    game.handle_special_food()

    assert len(game.special_foods) <= 2


def test_special_food_collision_gives_30_points(game_fixture):
    game = game_fixture
    game.score = 0
    sf = SpecialFood(position=game.snake.positions[0], remaining_ticks=10)
    game.special_foods = [sf]

    game.handle_special_food()

    assert game.score == 30


def test_special_food_collision_grows_snake_by_2(game_fixture):
    game = game_fixture
    initial_length = len(game.snake.positions)
    sf = SpecialFood(position=game.snake.positions[0], remaining_ticks=10)
    game.special_foods = [sf]

    game.handle_special_food()

    assert len(game.snake.positions) == initial_length + 2


def test_special_food_expires_after_countdown(game_fixture):
    game = game_fixture
    sf = SpecialFood(position=Position(99, 99), remaining_ticks=1)
    game.special_foods = [sf]

    game.handle_special_food()

    assert len(game.special_foods) == 0