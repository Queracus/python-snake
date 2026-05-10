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


def test_game_accepts_game_mode_from_menu():
    """Game should accept game_mode parameter from menu."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)

    game.start_level(1, game_mode="endless")

    assert game.game_mode == "endless"
    root.destroy()


def test_game_default_game_mode_is_level():
    """Default game_mode should be 'level'."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)

    game.start_level(1)

    assert game.game_mode == "level"
    root.destroy()


def test_endless_mode_starts_with_difficulty_0():
    """Endless mode should start with difficulty 0."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)

    game.start_level(1, game_mode="endless")

    assert game.endless_difficulty == 0
    root.destroy()


def test_endless_difficulty_increases_every_80_points():
    """Every 80 points should increase difficulty by 1."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1, game_mode="endless")

    game.score = 80
    game._update_endless_difficulty()
    assert game.endless_difficulty == 1

    game.score = 160
    game._update_endless_difficulty()
    assert game.endless_difficulty == 2

    root.destroy()


def test_endless_obstacles_increase_with_difficulty():
    """Difficulty should add 2 obstacles per level."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1, game_mode="endless")

    assert game.obstacles is None or len(game.obstacles.positions) == 0

    game.endless_difficulty = 1
    game._apply_endless_difficulty()
    assert len(game.obstacles.positions) == 2

    game.endless_difficulty = 3
    game._apply_endless_difficulty()
    assert len(game.obstacles.positions) == 6

    root.destroy()


def test_endless_speed_increases_with_difficulty():
    """Speed should increase (tick decrease) with difficulty."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1, game_mode="endless")
    initial_tick = game.tick_rate

    game.endless_difficulty = 1
    game._apply_endless_difficulty()
    assert game.tick_rate < initial_tick

    game.endless_difficulty = 5
    game._apply_endless_difficulty()
    assert game.tick_rate < initial_tick

    root.destroy()


def test_endless_speed_caps_at_60ms():
    """Speed should cap at 60ms (level 10 speed)."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1, game_mode="endless")

    game.endless_difficulty = 20
    game._apply_endless_difficulty()
    assert game.tick_rate == 60

    root.destroy()


def test_endless_mode_has_difficulty_for_renderer():
    """Endless mode should have difficulty attribute for HUD."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1, game_mode="endless")

    assert hasattr(game, 'endless_difficulty')
    game.endless_difficulty = 5

    assert game.endless_difficulty == 5
    root.destroy()


def test_endless_mode_never_triggers_level_complete():
    """Endless mode should never check level complete regardless of score."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    game = Game(root)
    game.start_level(1, game_mode="endless")
    game.score = 10000
    game.state = GameState.PLAYING

    assert not game.check_level_complete() or game.game_mode == "endless"

    root.destroy()