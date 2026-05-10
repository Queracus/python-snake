# PRD: Python Snake Game

## Problem Statement

The user wants an intermediate-level Snake game with a local Tkinter GUI. Key requirements:
- 10 levels with increasing difficulty (speed + obstacles)
- Level jump from menu (start at any level 1-10)
- Resizable window with dynamic play area that fills the window
- Controls: Arrow keys OR WASD (selectable)
- No sound
- Auto level transitions with countdown
- Endless mode with progressive difficulty

## Solution

A local desktop snake game using Python's Tkinter library with:
- Main menu for Start and Level Select
- 10 difficulty levels with increasing speed and obstacles
- Keyboard control schemes (arrows or WASD)
- Resizable window with play area that adapts to window size (expands AND contracts)
- Special bonus food that spawns periodically for extra points
- Auto level transitions with 4-second countdown
- Endless mode with progressive difficulty

## User Stories

### Core Game

1. As a player, I want a main menu with Start button, so that I can begin playing
2. As a player, I want to jump to any level (1-10), so that I can test difficulty
3. As a player, I want to choose between Arrow keys and WASD controls, so that I can use my preferred scheme
4. As a player, I want 10 levels with increasing speed, so that the game gets harder
5. As a player, I want obstacles that appear per level, so that I have more challenge
6. As a player, I want to see my current score, so that I know my progress
7. As a player, I want to see the current level, so that I know my progress
8. As a player, I want to see the score goal for the current level, so that I know what target to reach
9. As a player, I want game over on collision, so that there is a lose condition
10. As a player, I want to grow the snake by eating food, so that I progress in the game
11. As a player, I want to control direction with keyboard, so that I can change course
12. As a player, I want to see the snake, food, and obstacles rendered, so that I can play
13. As a player, I want to see why I died, so that I understand my mistakes

### Window Resizing

14. As a player, I want the play area to always match my window size, so that gameplay fills the entire window
15. As a player, I want the grid to expand in both directions when resizing larger, so that the play area fills the window
16. As a player, I want the grid to shrink in both directions when resizing smaller, so that gameplay stays within bounds
17. As a player, I want a minimum grid size of 20 cells in each dimension, so that the game never becomes unplayable
18. As a player, I want grid resizing to have no maximum limit, so that large displays can use the full screen
19. As a player, I want resizing during gameplay to be deferred, so that the grid only resizes at safe moments

### Special Food

20. As a player, I want special food to spawn periodically, so that I can earn bonus points
21. As a player, I want special food to be visually distinct (yellow), so that I can identify it quickly
22. As a player, I want special food to disappear after a time limit, so that I have to act quickly
23. As a player, I want special food to give more reward (30 points, +2 growth), so that it is worth chasing
24. As a player, I want at most 2 special foods on board, so that the game does not get too easy
25. As a player, I want special food timing to be consistent across levels in real-time, so that difficulty is fair

### Auto Level Transition

26. As a player, I want the game to automatically start the next level after a countdown so I don't have to press any key to continue.
27. As a player, I want to see a countdown timer on the screen during level transition so I know when the next level will start.
28. As a player, I want the game to return to the menu after completing level 10 with a countdown so the transition feels natural.

### Snake Spawn

29. As a player, I want the snake to spawn at least 7 cells away from any wall so I have time to react if the snake moves toward a wall.

### Endless Mode

30. As a player, I want to select "Endless Mode" from the menu so I can play an infinite game.
31. As a player, I want to see "Level Mode" option in the menu so I can play the traditional level-based game.
32. As a player, I want the level dropdown to only appear when Level Mode is selected so the UI is clean.
33. As a player, I want endless mode to add 2 obstacles every 80 points so the game gets harder.
34. As a player, I want endless mode to increase snake speed every 80 points so the game gets faster.
35. As a player, I want endless mode to cap speed at the level 10 speed (60ms) so the game stays playable.
36. As a player, I want endless mode to never reset obstacles or speed on game over so progress is truly endless.
37. As a player, I want to see the current difficulty level in endless mode so I know how hard the game is.
38. As a player, I want game over in endless mode to return to the menu so I can select mode again.

## Implementation Decisions

### Modules

| Module | Responsibility |
|--------|----------------|
| `game.py` | Game canvas, main loop, game state, resize handling, endless mode |
| `menu.py` | Main menu UI (Start button, Level Select, Control scheme, Game Mode) |
| `snake.py` | Snake entity (position, movement, growth, self-collision) |
| `food.py` | Food entities (normal + special food) |
| `obstacle.py` | Obstacle entity (per-level generation, collision) |
| `controls.py` | Input handling (key binding for arrows + WASD) |
| `renderer.py` | Canvas rendering (snake, food, obstacles, HUD, grid lines, countdown, difficulty) |
| `game_logic.py` | Collision detection functions |

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

- Snake: green connected rectangles (#00aa00)
- Normal food: red square (#ff0000)
- Special food: yellow square (#ffff00)
- Obstacles: gray squares (#666666)
- Grid boundary: subtle grid lines (#222222)
- HUD: score, level, goal, difficulty (endless mode), countdown (level transition)
- Canvas: fills window in both dimensions

### Special Food System

- Spawns every ~8 seconds (±1 second real-time) when fewer than 2 exist
- Visible duration: ~15 squares travel time (tick count adjusted per level to maintain constant real-time)
- Collision: +30 points, +2 snake growth
- Position validation: avoids snake body and normal food
- No immediate replacement on collection (waits for next interval)

### Level Configuration

| Level | Speed (ms) | Obstacles | Score Goal |
|-------|------------|-----------|------------|
| 1 | 150 | 0 | 50 |
| 2 | 140 | 2 | 60 |
| 3 | 130 | 4 | 70 |
| 4 | 120 | 6 | 80 |
| 5 | 110 | 8 | 90 |
| 6 | 100 | 10 | 100 |
| 7 | 90 | 12 | 110 |
| 8 | 80 | 14 | 120 |
| 9 | 70 | 16 | 130 |
| 10 | 60 | 18 | 140 |

### Game States

- **MENU** — Main menu displayed, resize recorded but not applied
- **PLAYING** — Active gameplay, resize deferred to next tick
- **GAME_OVER** — Death screen, resize deferred to next tick
- **LEVEL_COMPLETE** — Countdown to next level displayed, auto-transitions after 4 seconds

### Endless Mode

- Starts with 0 obstacles, speed 150ms (same as level 1)
- Every 80 points: difficulty increases by 1
- Each difficulty level: +2 obstacles, speed -10ms
- Speed caps at 60ms (level 10 speed)
- Difficulty persists during gameplay (obstacles accumulate)
- Never triggers level complete - plays continuously
- HUD shows "Diff: X" when difficulty > 0

### Snake Spawn

- Head spawns at least 7 cells from any wall (x: 7-12, y: 7-12 on 20x20 grid)
- Body extends 2 cells behind head in initial direction (RIGHT)

### Level Transition

- 4-second countdown after level complete
- Shows "Next level in X..." or "Returning to menu in X..."
- Auto-advances after countdown
- R key disabled during countdown

## Testing Decisions

Test external behavior only (not internal implementation details).

Priority modules for tests:
- `snake.py` — movement, growth, self-collision, spawn position
- `food.py` — spawn location validation, normal and special food
- `obstacle.py` — placement away from snake
- `game.py` — state transitions, scoring, special food timing, endless mode, countdown
- `renderer.py` — rendering correctness, difficulty display
- `menu.py` — game mode selector, level dropdown visibility

## Out of Scope

- Sound/audio
- High scores / leaderboard
- Multiple special food types
- Power-ups
- Multiple snake skins
- Network/multiplayer
- Persisting window size across sessions
- HUD scaling
- Custom countdown durations
- Visual themes for countdown display
- Different endless mode difficulty curves
- Endless mode specific power-ups

## Implementation History

### Initial Features (Project Launch)

- **Issue #2**: Basic Window + Canvas — Tkinter setup with 20x20 grid
- **Issue #3/#4**: Snake + Movement + Food + Eating — Snake entity, direction control, input mapping, food collision and growth
- **Issue #5**: Collision + Game Over — Game state transitions, collision detection, score on eat
- **Issue #6**: Main Menu — Tkinter frame UI with Start button, level select (1-10), control scheme toggle
- **Issue #7**: Levels + Obstacles — 10 levels with increasing speed and obstacles, obstacle collision
- **Issue #8**: Rendering + Game Loop — Canvas rendering, main game loop with tick, keyboard input
- **Level Progression**: Added score goal per level (50-140), goal display in HUD, LEVEL_COMPLETE state

### Bug Fixes

- **#9**: Game over showed no feedback — added death_cause to show collision type
- **#11**: Self-collision from rapid key presses — added direction queue system
- **#12**: Wall boundaries invisible — added grid line rendering
- **Snake Spawn**: Snake spawned pointing left causing immediate self-collision — spawns pointing RIGHT now
- **#14**: Grid never shrunk when window smaller — added contraction logic
- **#15**: Grid height not tracked during resize — added target_canvas_height
- **#16**: Grid reset to 20x20 after game over — show_menu() now adapts to window

### Features Added

- **#19**: Special Food — added bonus food with timed spawn (~8s interval, max 2), yellow color, 30pts/+2 growth, level-adjusted duration
- **#23-26**: Auto Level Transition with 4-second countdown, snake spawn at 7+ cells from wall, minimum grid size 20x20 enforced
- **#27-32**: Endless Mode with progressive difficulty, mode selector in menu, HUD difficulty display

### Completed Issues

| Issue | Title |
|-------|-------|
| #24 | Snake spawn: head ≥7 cells from any wall |
| #25 | Enforce minimum grid size 20x20 |
| #26 | Auto level transition with 4-second countdown |
| #28 | Menu: add game mode selector (Level/Endless) |
| #29 | Game: add game_mode and endless_difficulty attributes |
| #30 | Endless: difficulty increases every 80 points |
| #31 | Endless: display difficulty level in HUD |
| #32 | Endless: continuous play without level transition |