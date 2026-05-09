import tkinter as tk
from dataclasses import dataclass
from enum import Enum, auto
from controls import ControlScheme
from renderer import Renderer


LEVEL_CONFIG = {
    1: {"tick": 150, "obstacles": 0},
    2: {"tick": 140, "obstacles": 2},
    3: {"tick": 130, "obstacles": 4},
    4: {"tick": 120, "obstacles": 6},
    5: {"tick": 110, "obstacles": 8},
    6: {"tick": 100, "obstacles": 10},
    7: {"tick": 90, "obstacles": 12},
    8: {"tick": 80, "obstacles": 14},
    9: {"tick": 70, "obstacles": 16},
    10: {"tick": 60, "obstacles": 18},
}


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
        self.obstacles = None
        self.control_scheme = ControlScheme.ARROWS
        self.running = False
        self.menu = None

        self._setup_window()
        self._create_canvas()

    def _setup_window(self):
        self.root.title("Snake")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.root.bind("<Key>", self._on_key_press)

    def _create_canvas(self):
        self.canvas = tk.Canvas(
            self.root,
            width=self.grid.canvas_width,
            height=self.grid.canvas_height,
            bg="black"
        )
        self.canvas.pack(fill=tk.BOTH, expand=False)
        self.renderer = Renderer(self.canvas, self.grid.cell_size)

    def show_menu(self):
        from menu import create_menu

        self.canvas.pack_forget()
        self.menu = create_menu(self.root, self.on_start_game)
        self.menu.show()

    def on_start_game(self, level: int, control_scheme: ControlScheme):
        self.level = level
        self.control_scheme = control_scheme
        self.start_level(level)

    def start_level(self, level: int):
        from snake import Snake
        from food import Food
        from obstacles import Obstacles

        self.level = level
        self.score = 0
        self.snake = Snake(grid_width=self.grid.width, grid_height=self.grid.height)
        self.food = Food.create(
            grid_width=self.grid.width,
            grid_height=self.grid.height,
            snake_positions=self.snake.positions
        )
        obstacle_count = LEVEL_CONFIG[level]["obstacles"]
        self.obstacles = Obstacles.create(
            grid_width=self.grid.width,
            grid_height=self.grid.height,
            count=obstacle_count,
            snake_positions=self.snake.positions
        )
        self.state = GameState.PLAYING
        self.tick_rate = LEVEL_CONFIG[level]["tick"]
        self.running = True

        self.show_game_canvas()
        self._game_loop()

    def show_game_canvas(self):
        if not self.menu:
            return
        self.menu.hide()
        self.canvas.pack(fill=tk.BOTH, expand=False)

    def _game_loop(self):
        if not self.running or self.state != GameState.PLAYING:
            return

        self.snake.move()
        self.check_collisions()
        self.handle_eat()
        self._render()

        if self.state == GameState.PLAYING:
            self.root.after(self.tick_rate, self._game_loop)
        elif self.state == GameState.GAME_OVER:
            self._render_game_over()

    def _render(self):
        if self.snake and self.food and self.obstacles:
            self.renderer.render(self.snake, self.food, self.obstacles, self.score, self.level)

    def _render_game_over(self):
        self.renderer.render_game_over(self.score)

    def _on_key_press(self, event):
        if self.state != GameState.PLAYING:
            if event.keysym == "r" or event.keysym == "R":
                self.restart()
            return

        from controls import map_key_to_direction
        from snake import Direction

        direction = map_key_to_direction(event.keysym, self.control_scheme)
        if direction:
            self.snake.change_direction(direction)

    def restart(self):
        if hasattr(self, 'menu') and self.menu:
            self.show_menu()
        else:
            self.start_level(self.level)

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

        if self.obstacles:
            if self.obstacles.check_collision(head):
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
        self.show_menu()
        self.root.mainloop()


def main():
    root = tk.Tk()
    game = Game(root)
    game.start()


if __name__ == "__main__":
    main()