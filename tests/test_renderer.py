import pytest
import tkinter as tk
from renderer import Renderer


def test_grid_boundary_visible_on_render():
    """When render() is called, grid lines should be present on canvas."""
    root = tk.Tk()
    root.withdraw()
    canvas = tk.Canvas(root, width=400, height=400, bg="black")
    renderer = Renderer(canvas, cell_size=20)

    from snake import Snake
    from food import Food
    from obstacles import Obstacles

    snake = Snake(grid_width=20, grid_height=20)
    food = Food.create(grid_width=20, grid_height=20)
    obstacles = Obstacles.create(grid_width=20, grid_height=20, count=0)

    renderer.render(snake, food, obstacles, score=0, level=1, goal=50)

    all_items = canvas.find_all()
    line_items = [i for i in all_items if canvas.type(i) == "line"]
    assert len(line_items) >= 38, f"Expected at least 38 grid lines (19 vertical + 19 horizontal), got {len(line_items)}"

    root.destroy()