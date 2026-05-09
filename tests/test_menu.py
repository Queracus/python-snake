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

    def on_start(level, controls):
        result["level"] = level
        result["controls"] = controls

    menu = create_menu(root, on_start)
    menu.selected_level.set(7)
    menu.selected_controls.set(1)
    menu._on_start_clicked()

    assert result["level"] == 7
    assert result["controls"] == ControlScheme.WASD
    root.destroy()