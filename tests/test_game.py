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


def test_level_complete_triggers_countdown():
    """When level completes, game should enter countdown state."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1)
    game.score = 100  # Exceed goal
    game.state = GameState.PLAYING

    # Simulate level complete check
    if game.check_level_complete():
        game.state = GameState.LEVEL_COMPLETE
        game._start_countdown()

    assert hasattr(game, 'countdown_remaining')
    assert game.countdown_remaining == 4
    root.destroy()


def test_countdown_auto_transitions_to_next_level():
    """After countdown completes, should auto-transition to next level."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1)
    game.level = 1
    game.countdown_remaining = 1
    game.countdown_timer = 1000  # Force timer to trigger decrement
    game.state = GameState.LEVEL_COMPLETE

    game._tick_countdown()

    assert game.level == 2
    assert game.state == GameState.PLAYING
    root.destroy()


def test_countdown_auto_transitions_to_menu_after_level_10():
    """After level 10 countdown, should return to menu."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(10)
    game.level = 10
    game.countdown_remaining = 1
    game.countdown_timer = 1000  # Force timer to trigger decrement
    game.state = GameState.LEVEL_COMPLETE

    game._tick_countdown()

    assert game.state == GameState.MENU
    root.destroy()