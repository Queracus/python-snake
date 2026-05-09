import pytest
import tkinter as tk
from dataclasses import dataclass


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


def test_grid_dimensions():
    grid = Grid()
    assert grid.width == 20
    assert grid.height == 20
    assert grid.cell_size == 20
    assert grid.canvas_width == 400
    assert grid.canvas_height == 400