import pytest
from game import Game, GameState
from snake import Snake, Position
from food import Food


def test_game_over_on_wall_collision():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1)
    game.snake.positions[0] = Position(20, 10)

    game.check_collisions()

    assert game.state == GameState.GAME_OVER
    root.destroy()


def test_game_over_on_self_collision():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1)
    game.snake.positions = [
        Position(10, 10),
        Position(10, 9),
        Position(10, 10),
    ]

    game.check_collisions()

    assert game.state == GameState.GAME_OVER
    root.destroy()


def test_score_increases_on_eat():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1)
    game.food.position = game.snake.positions[0]

    game.handle_eat()

    assert game.score == 10
    root.destroy()