import tkinter as tk
from typing import Optional, List
from snake import Snake, Position
from food import Food, SpecialFood
from obstacles import Obstacles


class Renderer:
    def __init__(self, canvas: tk.Canvas, cell_size: int = 20):
        self.canvas = canvas
        self.cell_size = cell_size
        self._score_text_id: Optional[int] = None
        self._level_text_id: Optional[int] = None

    def clear(self):
        self.canvas.delete("all")
        self._score_text_id = None
        self._level_text_id = None

    def render(self, snake: Snake, food: Food, obstacles: Obstacles, score: int, level: int, goal: int = 50, special_foods: Optional[List[SpecialFood]] = None):
        self.clear()
        self._render_grid_boundary()
        self._render_obstacles(obstacles)
        self._render_food(food)
        if special_foods:
            self._render_special_foods(special_foods)
        self._render_snake(snake)
        self._render_hud(score, level, goal)

    def _render_grid_boundary(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10:
            w = int(self.canvas.cget("width"))
        if h < 10:
            h = int(self.canvas.cget("height"))
        grid_color = "#222222"
        for x in range(0, w + 1, self.cell_size):
            self.canvas.create_line(x, 0, x, h, fill=grid_color)
        for y in range(0, h + 1, self.cell_size):
            self.canvas.create_line(0, y, w, y, fill=grid_color)

    def _render_snake(self, snake: Snake):
        for pos in snake.positions:
            x1 = pos.x * self.cell_size
            y1 = pos.y * self.cell_size
            x2 = x1 + self.cell_size - 1
            y2 = y1 + self.cell_size - 1
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#00aa00",
                outline="#00dd00"
            )

    def _render_food(self, food: Food):
        x1 = food.position.x * self.cell_size
        y1 = food.position.y * self.cell_size
        x2 = x1 + self.cell_size - 1
        y2 = y1 + self.cell_size - 1
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill="#ff0000",
            outline="#ff3333"
        )

    def _render_special_foods(self, special_foods: List[SpecialFood]):
        for sf in special_foods:
            x1 = sf.position.x * self.cell_size
            y1 = sf.position.y * self.cell_size
            x2 = x1 + self.cell_size - 1
            y2 = y1 + self.cell_size - 1
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#ffff00",
                outline="#ffff33"
            )

    def _render_obstacles(self, obstacles: Obstacles):
        for pos in obstacles.positions:
            x1 = pos.x * self.cell_size
            y1 = pos.y * self.cell_size
            x2 = x1 + self.cell_size - 1
            y2 = y1 + self.cell_size - 1
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="#666666",
                outline="#444444"
            )

    def _render_hud(self, score: int, level: int, goal: int = 50):
        self.canvas.create_text(
            10, 10,
            text=f"Score: {score}",
            fill="white",
            anchor="nw",
            font=("Arial", 12, "bold")
        )
        self.canvas.create_text(
            10, 30,
            text=f"Level: {level}",
            fill="white",
            anchor="nw",
            font=("Arial", 12, "bold")
        )
        self.canvas.create_text(
            10, 50,
            text=f"Goal: {goal}",
            fill="#aaaaaa",
            anchor="nw",
            font=("Arial", 10)
        )

    def render_game_over(self, score: int, cause: str = ""):
        if cause:
            message = f"GAME OVER\n{cause}\nScore: {score}\nPress R to Restart"
        else:
            message = f"GAME OVER\nScore: {score}\nPress R to Restart"
        
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=message,
            fill="white",
            font=("Arial", 24, "bold"),
            justify="center"
        )

    def render_level_complete(self, level: int):
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=f"LEVEL {level} COMPLETE!\nPress R for Next Level",
            fill="#00ff00",
            font=("Arial", 24, "bold"),
            justify="center"
        )