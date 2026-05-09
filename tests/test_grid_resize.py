import pytest
import tkinter as tk
from game import Game, Grid


def test_grid_width_and_height_update_from_window_size():
    """When starting a level, grid width and height should reflect the current canvas size."""
    root = tk.Tk()
    root.geometry("600x500")
    root.update()

    game = Game(root)
    game.grid.min_width = 600 // 20
    game.grid.min_height = 500 // 20
    game.grid.recompute(600, 500)
    game.canvas.config(width=game.grid.canvas_width, height=game.grid.canvas_height)
    game.start_level(1)
    root.update()

    assert game.grid.width == 30, f"Expected width 30 (600/20), got {game.grid.width}"
    assert game.grid.height == 25, f"Expected height 25 (500/20), got {game.grid.height}"

    root.destroy()


def test_grid_resets_to_default_20_on_new_game():
    """Starting a new game from menu resets grid to default 20x20."""
    root = tk.Tk()
    root.geometry("600x500")
    root.update()

    game = Game(root)
    game.grid.min_width = 600 // 20
    game.grid.min_height = 500 // 20
    game.grid.recompute(600, 500)
    game.canvas.config(width=game.grid.canvas_width, height=game.grid.canvas_height)
    game.start_level(1)
    root.update()

    assert game.grid.width == 30
    assert game.grid.height == 25

    game.show_menu()
    game.on_start_game(1, game.control_scheme)
    root.update()

    assert game.grid.width == 20, f"Expected reset to 20, got {game.grid.width}"
    assert game.grid.height == 20, f"Expected reset to 20, got {game.grid.height}"

    root.destroy()


def test_restart_keeps_current_grid_size():
    """Restarting within a level keeps the current grid size (does not reset)."""
    root = tk.Tk()
    root.geometry("600x500")
    root.update()

    game = Game(root)
    game.grid.min_width = 600 // 20
    game.grid.min_height = 500 // 20
    game.grid.recompute(600, 500)
    game.canvas.config(width=game.grid.canvas_width, height=game.grid.canvas_height)
    game.start_level(1)
    root.update()

    assert game.grid.width == 30
    assert game.grid.height == 25

    game.state = game.state.GAME_OVER
    game.restart()
    root.update()

    assert game.grid.width == 30, f"Expected 30 (kept), got {game.grid.width}"
    assert game.grid.height == 25, f"Expected 25 (kept), got {game.grid.height}"

    root.destroy()