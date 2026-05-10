# PRD: Python Snake Game

## Problem Statement

The user wants an intermediate-level Snake game with a local Tkinter GUI. Key requirements:
- 10 levels with increasing difficulty (speed + obstacles)
- Level jump from menu (start at any level 1-10)
- Resizable window with dynamic play area that fills the window
- Controls: Arrow keys OR WASD (selectable)
- No sound

## Solution

A local desktop snake game using Python's Tkinter library with:
- Main menu for Start and Level Select
- 10 difficulty levels with increasing speed and obstacles
- Keyboard control schemes (arrows or WASD)
- Resizable window with play area that adapts to window size (expands AND contracts)

## User Stories

### Core Game

1. As a player, I want a main menu with Start button, so that I can begin playing
2. As a player, I want to jump to any level (1-10), so that I can test difficulty
3. As a player, I want to choose between Arrow keys and WASD controls, so that I can use my preferred scheme
4. As a player, I want 10 levels with increasing speed, so that the game gets harder
5. As a player, I want obstacles that appear per level, so that I have more challenge
6. As a player, I want to see my current score, so that I know my progress
7. As a player, I want to see the current level, so that I know my progress
8. As a player, I want game over on collision, so that there is a lose condition
9. As a player, I want to grow the snake by eating food, so that I progress in the game
10. As a player, I want to control direction with keyboard, so that I can change course
11. As a player, I want to see the snake, food, and obstacles rendered, so that I can play
12. As a player, I want to see why I died, so that I understand my mistakes

### Window Resizing

13. As a player, I want the play area to always match my window size, so that gameplay fills the entire window
14. As a player, I want the grid to expand in both directions when resizing larger, so that the play area fills the window
15. As a player, I want the grid to shrink in both directions when resizing smaller, so that gameplay stays within bounds
16. As a player, I want a minimum grid size of 20 cells in each dimension, so that the game never becomes unplayable
17. As a player, I want grid resizing to have no maximum limit, so that large displays can use the full screen
18. As a player, I want resizing during gameplay to be deferred, so that the grid only resizes at safe moments

## Game States

- **MENU** — Main menu displayed, resize recorded but not applied
- **PLAYING** — Active gameplay, resize deferred to next tick
- **GAME_OVER** — Death screen, resize deferred to next tick
- **LEVEL_COMPLETE** — "Press R for Next Level" shown, `_expand_grid_if_needed()` called here

## Implementation Decisions

### Modules

| Module | Responsibility |
|--------|----------------|
| `main.py` | Tkinter root window, app initialization |
| `menu.py` | Main menu UI (Start button, Level Select, Control scheme) |
| `game.py` | Game canvas, main loop, game state, resize handling |
| `snake.py` | Snake entity (position, movement, growth, self-collision) |
| `food.py` | Food entity (random placement, collision detection) |
| `obstacle.py` | Obstacle entity (per-level generation, collision) |
| `controls.py` | Input handling (key binding for arrows + WASD) |
| `renderer.py` | Canvas rendering (snake, food, obstacles, HUD) |

### Grid System

- **cell_size = 20px** — fixed, never changes
- **grid.width, grid.height** — in cells, adjusts to window size
- **Canvas dimensions** = grid.width * cell_size, grid.height * cell_size
- Grid expands AND contracts to match window size
- Minimum: 20 cells per dimension (enforced even if window is very small)
- Maximum: unlimited (grid fills window)

### Resize Mechanism

1. `<Configure>` event on root window records `target_canvas_width` AND `target_canvas_height`
2. `_expand_grid_if_needed()` called at safe moments:
   - Each game loop tick (during PLAYING, GAME_OVER)
   - LEVEL_COMPLETE render
   - MENU show
3. Only updates grid if new size differs; minimum 20 cells enforced

### Rendering

- Snake: green connected rectangles
- Food: red square
- Obstacles: gray/brown squares
- Grid boundary: subtle grid lines (#222222)
- HUD: score and level text at fixed pixel coordinates (10, 10)
- Canvas: `fill=tk.BOTH, expand=True` — fills window in both dimensions

### Level Configuration

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

### Direction Input

- **Direction input is queued** — only one direction change per tick
- `pending_direction` stores queued input, applied on next tick
- Prevents self-collision from rapid key presses

## Testing Decisions

Priority modules for tests:
- `snake.py` — movement, growth, self-collision
- `food.py` — spawn location not on snake
- `obstacle.py` — placement away from snake
- `test_grid_resize.py` — window resize behavior

Test external behavior only (not internal state).

## Out of Scope

- Sound/audio
- High scores / leaderboard
- Power-ups
- Multiple snake skins
- Network/multiplayer
- Persisting window size across sessions
- HUD scaling

## Historical Bug Fixes

### Bug Fix #11 — Self-collision from rapid key presses

**Problem:** Rapid direction key presses caused snake to turn into its own body.

**Fix:** Queued direction system — `pending_direction` stores one queued input per tick.

### Bug Fix #14 — Grid overflow when resizing smaller on level complete

**Problem:** Grid expanded but never contracted when resizing smaller.

**Fix:** Added `elif` branches in `_expand_grid_if_needed()` to handle shrinking with minimum 20-cell constraint.

### Bug Fix #15 — Grid height not tracked during resize

**Problem:** Only `target_canvas_width` was tracked, height changes were ignored.

**Fix:** Added `target_canvas_height` tracking and updated `_expand_grid_if_needed()` to handle both dimensions.

### Bug Fix #16 — Grid resets to default after game over

**Problem:** Returning to menu hard-reset grid to 20x20, ignoring window size.

**Fix:** `show_menu()` now calls `_expand_grid_if_needed()` instead of hard-resetting.
