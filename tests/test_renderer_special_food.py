import tkinter as tk
from renderer import Renderer
from snake import Snake, Position
from food import Food, SpecialFood
from obstacles import Obstacles


def test_renderer_accepts_special_foods():
    root = tk.Tk()
    root.withdraw()
    canvas = tk.Canvas(root, width=400, height=400)
    renderer = Renderer(canvas, cell_size=20)

    snake = Snake(grid_width=20, grid_height=20)
    food = Food.create(grid_width=20, grid_height=20)
    obstacles = Obstacles.create(grid_width=20, grid_height=20, count=0)

    special_foods = [
        SpecialFood(position=Position(5, 5), remaining_ticks=10),
        SpecialFood(position=Position(10, 10), remaining_ticks=10),
    ]

    renderer.render(snake, food, obstacles, score=0, level=1, goal=50, special_foods=special_foods)

    root.destroy()