import tkinter as tk
from dataclasses import dataclass
from enum import Enum, auto


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


@dataclass
class Grid:
    width: int = 20
    height: int = 20
    cell_size: int = 20

    @property
    def canvas_width(self) -> int:
        return self.width * self.cell_size

    @property
    def canvas_height(self) -> int:
        return self.height * self.cell_size


class Game:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.state = GameState.MENU
        self.grid = Grid()
        self.tick_rate = 150
        self.score = 0
        self.level = 1
        self.snake = None
        self.food = None

        self._setup_window()
        self._create_canvas()

    def _setup_window(self):
        self.root.title("Snake")
        self.root.geometry("600x600")
        self.root.resizable(True, True)

    def _create_canvas(self):
        self.canvas = tk.Canvas(
            self.root,
            width=self.grid.canvas_width,
            height=self.grid.canvas_height,
            bg="black"
        )
        self.canvas.pack(fill=tk.BOTH, expand=False)

    def start_level(self, level: int):
        from snake import Snake
        from food import Food

        self.level = level
        self.score = 0
        self.snake = Snake(grid_width=self.grid.width, grid_height=self.grid.height)
        self.food = Food.create(
            grid_width=self.grid.width,
            grid_height=self.grid.height,
            snake_positions=self.snake.positions
        )
        self.state = GameState.PLAYING
        self.tick_rate = self._get_tick_rate(level)

    def _get_tick_rate(self, level: int) -> int:
        return 160 - (level * 10)

    def check_collisions(self):
        if not self.snake:
            return

        head = self.snake.positions[0]

        from game_logic import check_wall_collision, check_self_collision, check_food_collision

        if check_wall_collision(head, self.grid.width, self.grid.height):
            self.state = GameState.GAME_OVER
            return

        if check_self_collision(self.snake.positions):
            self.state = GameState.GAME_OVER
            return

    def handle_eat(self):
        if not self.snake or not self.food:
            return

        from game_logic import check_food_collision
        if check_food_collision(self.snake.positions[0], self.food.position):
            self.score += self.food.eat()
            self.snake.positions.append(self.snake.positions[-1])
            self.food.respawn(
                grid_width=self.grid.width,
                grid_height=self.grid.height,
                snake_positions=self.snake.positions
            )

    def start(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    game = Game(root)
    game.start()


if __name__ == "__main__":
    main()