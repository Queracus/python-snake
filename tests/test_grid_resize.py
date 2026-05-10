import pytest
import tkinter as tk
from game import Game, Grid, GameState


def test_game_starts_without_crash():
    """Game should start level without immediately crashing."""
    root = tk.Tk()
    root.geometry("600x600")
    root.update()

    game = Game(root)
    game.show_menu()
    game.on_start_game(1, game.control_scheme)
    root.update()

    assert game.state != GameState.GAME_OVER or len(game.snake.positions) <= 2

    root.destroy()


def test_game_starts_in_playing_state():
    """Starting a level should put game in PLAYING state with valid snake."""
    root = tk.Tk()
    root.geometry("600x600")
    root.update()

    game = Game(root)
    game.show_menu()
    game.on_start_game(1, game.control_scheme)
    root.update()

    assert game.snake is not None
    assert len(game.snake.positions) >= 3
    assert game.state == GameState.PLAYING

    root.destroy()


def test_grid_height_respects_window_height():
    """Grid height should expand when window height increases."""
    root = tk.Tk()
    root.geometry("400x800")
    root.update()

    game = Game(root)
    game.show_menu()
    game.on_start_game(1, game.control_scheme)
    root.update()

    # Simulate resize to tall window
    game._on_resize(type('Event', (), {'width': 400, 'height': 800})())
    game._expand_grid_if_needed()

    assert game.grid.height >= 40  # 800 // 20 = 40

    root.destroy()


def test_grid_width_respects_window_width():
    """Grid width should expand when window width increases."""
    root = tk.Tk()
    root.geometry("400x400")
    root.update()

    game = Game(root)
    game.show_menu()
    game.on_start_game(1, game.control_scheme)
    root.update()

    # Simulate resize to wide window
    game._on_resize(type('Event', (), {'width': 800, 'height': 400})())
    game._expand_grid_if_needed()

    assert game.grid.width >= 40  # 800 // 20 = 40

    root.destroy()