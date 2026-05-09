import pytest
import tkinter as tk
from game import Game, GameState


def test_resize_during_playing_is_deferred():
    """Resize during PLAYING state should be deferred, not applied immediately."""
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

    fake_event = tk.Event()
    fake_event.width = 800
    fake_event.height = 600
    game._on_resize(fake_event)
    root.update()

    assert game.grid.width == 30, f"Expected 30 (deferred), got {game.grid.width}"
    assert game._pending_width == 800

    root.destroy()


def test_deferred_resize_applied_on_level_complete():
    """Deferred resize should be applied when entering LEVEL_COMPLETE via render."""
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

    fake_event = tk.Event()
    fake_event.width = 800
    fake_event.height = 600
    game._on_resize(fake_event)

    game.state = GameState.LEVEL_COMPLETE
    fake_event2 = tk.Event()
    fake_event2.width = 800
    fake_event2.height = 600
    game._on_resize(fake_event2)

    game._render_level_complete()
    root.update()

    assert game.grid.width == 40, f"Expected 40, got {game.grid.width}"
    assert game.grid.height == 30, f"Expected 30, got {game.grid.height}"

    root.destroy()


def test_resize_on_level_complete_updates_min():
    """Resizing on LEVEL_COMPLETE updates the minimum for the next level."""
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

    game.state = GameState.LEVEL_COMPLETE

    fake_event = tk.Event()
    fake_event.width = 800
    fake_event.height = 600
    game._on_resize(fake_event)
    root.update()

    game._render_level_complete()
    root.update()

    assert game.grid.min_width == 40, f"Expected min_width 40, got {game.grid.min_width}"
    assert game.grid.min_height == 30, f"Expected min_height 30, got {game.grid.min_height}"

    root.destroy()