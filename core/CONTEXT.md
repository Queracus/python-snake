# Core Context

Core domain for python-snake.

## Domain Language

- **Snake** — the player-controlled snake
- **Food** — collectible items that grow the snake
- **Grid** — the game board (cell_size=20px fixed; width/height in cells adjusts to window size, expands AND contracts with minimum 20x20)
- **Score** — points earned from collecting food
- **Level** — difficulty tier (1-10)
- **Obstacle** — static blocks that kill the snake on collision
- **Game State** — MENU, PLAYING, PAUSED, GAME_OVER

## Key Concepts

- 10 levels with increasing difficulty (speed + obstacles)
- Level jump from menu (start at any level 1-10)
- Controls: Arrow keys OR WASD (selectable in menu)
- Resizable window, fixed game area
- No sound

## Level Progression

| Level | Speed (ms) | Obstacles |
|-------|------------|-----------|
| 1 | 150 | 0 |
| 2 | 140 | 2 |
| 3 | 130 | 4 |
| 4 | 120 | 6 |
| 5 | 110 | 8 |
| 6 | 100 | 10 |
| 7 | 90 | 12 |
| 8 | 80 | 14 |
| 9 | 70 | 16 |
| 10 | 60 | 18 |

## Components

- `main.py` — app entry, Tkinter window
- `menu.py` — main menu UI (start, level select)
- `game.py` — game canvas and loop
- `snake.py` — snake entity (movement, growth, collision)
- `food.py` — food spawning
- `obstacle.py` — obstacle management per level
- `controls.py` — input handling (arrows/WASD)