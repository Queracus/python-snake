import tkinter as tk
from typing import Optional
from snake import Snake, Position
from food import Food
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

    def render(self, snake: Snake, food: Food, obstacles: Obstacles, score: int, level: int):
        self.clear()
        self._render_obstacles(obstacles)
        self._render_food(food)
        self._render_snake(snake)
        self._render_hud(score, level)

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

    def _render_hud(self, score: int, level: int):
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

    def render_game_over(self, score: int):
        self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=f"GAME OVER\nScore: {score}\nPress R to Restart",
            fill="white",
            font=("Arial", 24, "bold"),
            justify="center"
        )