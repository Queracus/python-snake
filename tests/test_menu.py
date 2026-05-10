import pytest
from menu import MainMenu, create_menu
from controls import ControlScheme


def test_menu_initial_level():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    def on_start(level, controls):
        pass

    menu = create_menu(root, on_start)
    assert menu.selected_level.get() == 1
    root.destroy()


def test_menu_can_change_level():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    def on_start(level, controls):
        pass

    menu = create_menu(root, on_start)
    menu.selected_level.set(5)

    assert menu.selected_level.get() == 5
    root.destroy()


def test_menu_default_controls():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    def on_start(level, controls):
        pass

    menu = create_menu(root, on_start)
    assert menu.selected_controls.get() == 0
    root.destroy()


def test_menu_callback_with_level_and_controls():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    result = {}

    def on_start(level, controls, game_mode):
        result["level"] = level
        result["controls"] = controls
        result["game_mode"] = game_mode

    menu = create_menu(root, on_start)
    menu.selected_level.set(7)
    menu.selected_controls.set(1)
    menu._on_start_clicked()

    assert result["level"] == 7
    assert result["controls"] == ControlScheme.WASD
    assert result["game_mode"] == "level"
    root.destroy()


def test_menu_has_game_mode_selector():
    """Menu should have game_mode selector with level/endless options."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    def on_start(level, controls, game_mode):
        pass

    menu = create_menu(root, on_start)
    assert hasattr(menu, 'selected_game_mode')
    assert menu.selected_game_mode.get() == "level"
    root.destroy()


def test_menu_endless_mode_changes_widget_visibility():
    """Endless mode should call pack_forget on level widgets."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    def on_start(level, controls, game_mode):
        pass

    menu = create_menu(root, on_start)

    menu.selected_game_mode.set("endless")
    menu._on_game_mode_changed()

    menu.selected_game_mode.set("level")
    menu._on_game_mode_changed()

    root.destroy()


def test_menu_callback_includes_game_mode():
    """Callback should receive game_mode parameter."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()

    result = {}

    def on_start(level, controls, game_mode):
        result["level"] = level
        result["controls"] = controls
        result["game_mode"] = game_mode

    menu = create_menu(root, on_start)
    menu.selected_game_mode.set("endless")
    menu._on_start_clicked()

    assert result["game_mode"] == "endless"
    root.destroy()