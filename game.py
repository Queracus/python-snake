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

    def start(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    game = Game(root)
    game.start()


if __name__ == "__main__":
    main()