import tkinter as tk
import random
from dataclasses import dataclass
from enum import Enum, auto
from controls import ControlScheme
from renderer import Renderer


LEVEL_CONFIG = {
    1: {"tick": 150, "obstacles": 0, "goal": 50},
    2: {"tick": 140, "obstacles": 2, "goal": 60},
    3: {"tick": 130, "obstacles": 4, "goal": 70},
    4: {"tick": 120, "obstacles": 6, "goal": 80},
    5: {"tick": 110, "obstacles": 8, "goal": 90},
    6: {"tick": 100, "obstacles": 10, "goal": 100},
    7: {"tick": 90, "obstacles": 12, "goal": 110},
    8: {"tick": 80, "obstacles": 14, "goal": 120},
    9: {"tick": 70, "obstacles": 16, "goal": 130},
    10: {"tick": 60, "obstacles": 18, "goal": 140},
}


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    LEVEL_COMPLETE = auto()
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
        self.special_foods = []
        self.special_food_spawn_timer = 0
        self.special_food_spawn_interval = 8000
        self.control_scheme = ControlScheme.ARROWS
        self.running = False
        self.menu = None
        self.death_cause = ""
        self.target_canvas_width = 400
        self.target_canvas_height = 400
        self.countdown_remaining = 0
        self.countdown_timer = 0

        self._setup_window()
        self._create_canvas()

    def _setup_window(self):
        self.root.title("Snake")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Configure>", self._on_resize)

    def _create_canvas(self):
        self.canvas = tk.Canvas(
            self.root,
            width=self.grid.canvas_width,
            height=self.grid.canvas_height,
            bg="black"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.renderer = Renderer(self.canvas, self.grid.cell_size)

    def _on_resize(self, event):
        if event.width == 1 and event.height == 1:
            return
        self.target_canvas_width = event.width
        self.target_canvas_height = event.height

    def _expand_grid_if_needed(self):
        new_width = self.target_canvas_width // self.grid.cell_size
        new_height = self.target_canvas_height // self.grid.cell_size
        if new_width > self.grid.width:
            self.grid.width = new_width
            self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)
        elif new_width < self.grid.width and new_width >= 20:
            self.grid.width = new_width
            self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)
        if new_height > self.grid.height:
            self.grid.height = new_height
            self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)
        elif new_height < self.grid.height and new_height >= 20:
            self.grid.height = new_height
            self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)

    def show_menu(self):
        from menu import create_menu

        self._expand_grid_if_needed()
        self.canvas.pack_forget()
        self.menu = create_menu(self.root, self.on_start_game)
        self.menu.show()
        self.state = GameState.MENU

    def on_start_game(self, level: int, control_scheme: ControlScheme):
        self.level = level
        self.control_scheme = control_scheme
        self.start_level(level)

    def start_level(self, level: int):
        from snake import Snake
        from food import Food
        from obstacles import Obstacles

        self._expand_grid_if_needed()

        self.level = level
        self.score = 0
        self.death_cause = ""
        self.snake = Snake(grid_width=self.grid.width, grid_height=self.grid.height)
        self.food = Food.create(
            grid_width=self.grid.width,
            grid_height=self.grid.height,
            snake_positions=self.snake.positions
        )
        self.special_foods = []
        self.special_food_spawn_timer = 0
        self.special_food_spawn_interval = 8000
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
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self._expand_grid_if_needed()

    def _game_loop(self):
        if not self.running or self.state != GameState.PLAYING:
            return

        self._expand_grid_if_needed()

        self.snake.move()
        self.check_collisions()
        self.handle_eat()
        self.handle_special_food()

        if self.state == GameState.GAME_OVER:
            self._render_game_over()
            return

        if self.check_level_complete():
            self.state = GameState.LEVEL_COMPLETE
            self._start_countdown()
            return

        self._render()

        if self.state == GameState.PLAYING:
            self.root.after(self.tick_rate, self._game_loop)

    def _render(self):
        if self.snake and self.food and self.obstacles:
            goal = LEVEL_CONFIG[self.level]["goal"]
            self.renderer.render(self.snake, self.food, self.obstacles, self.score, self.level, goal, self.special_foods)

    def _render_game_over(self):
        self.renderer.render_game_over(self.score, self.death_cause)

    def _render_level_complete(self):
        self._expand_grid_if_needed()
        self.renderer.render_level_complete(self.level)

    def _on_key_press(self, event):
        if self.state == GameState.GAME_OVER:
            if event.keysym == "r" or event.keysym == "R":
                self.restart()
            return

        if self.state == GameState.LEVEL_COMPLETE:
            return  # Ignore all input during countdown (automatic)

        if self.state != GameState.PLAYING:
            return

        from controls import map_key_to_direction
        from snake import Direction

        direction = map_key_to_direction(event.keysym, self.control_scheme)
        if direction:
            self.snake.change_direction(direction)

    def next_level(self):
        if self.level < 10:
            self.start_level(self.level + 1)
        else:
            self.show_menu()

    def _start_countdown(self):
        self.countdown_remaining = 4
        self.countdown_timer = 0
        self._render_countdown()
        self.root.after(self.tick_rate, lambda: self._tick_countdown())

    def _tick_countdown(self):
        self.countdown_timer += self.tick_rate
        if self.countdown_timer >= 1000:
            self.countdown_timer = 0
            self.countdown_remaining -= 1

            if self.countdown_remaining <= 0:
                self.next_level()
                return

        if self.countdown_remaining > 0:
            self._render_countdown()
            self.root.after(self.tick_rate, lambda: self._tick_countdown())

    def _render_countdown(self):
        if self.level < 10:
            message = f"Next level in {self.countdown_remaining}..."
        else:
            message = f"Returning to menu in {self.countdown_remaining}..."
        self._expand_grid_if_needed()
        self.renderer.render_countdown(message, self.level)

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
            self.death_cause = "You hit the wall!"
            return

        if check_self_collision(self.snake.positions):
            self.state = GameState.GAME_OVER
            self.death_cause = "You hit yourself!"
            return

        if self.obstacles:
            if self.obstacles.check_collision(head):
                self.state = GameState.GAME_OVER
                self.death_cause = "You hit an obstacle!"
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

    def handle_special_food(self):
        if not self.snake:
            return

        self.special_food_spawn_timer += self.tick_rate
        interval_with_jitter = self.special_food_spawn_interval + random.randint(-1000, 1000)

        if len(self.special_foods) < 2 and self.special_food_spawn_timer >= interval_with_jitter:
            from food import SpecialFood
            new_special = SpecialFood.create(
                grid_width=self.grid.width,
                grid_height=self.grid.height,
                snake_positions=self.snake.positions,
                food_position=self.food.position if self.food else None,
                tick_rate=self.tick_rate
            )
            self.special_foods.append(new_special)
            self.special_food_spawn_timer = 0

        head = self.snake.positions[0]
        uneaten_specials = []
        for sf in self.special_foods:
            if head.x == sf.position.x and head.y == sf.position.y:
                self.score += sf.eat()
                for _ in range(sf.growth_amount):
                    self.snake.positions.append(self.snake.positions[-1])
            else:
                if sf.tick():
                    uneaten_specials.append(sf)
        self.special_foods = uneaten_specials

    def check_level_complete(self) -> bool:
        goal = LEVEL_CONFIG[self.level]["goal"]
        return self.score >= goal

    def start(self):
        self.show_menu()
        self.root.mainloop()


def main():
    root = tk.Tk()
    game = Game(root)
    game.start()


if __name__ == "__main__":
    main()