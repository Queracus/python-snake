## Problem Statement

The user wants an intermediate-level Snake game with a local Tkinter GUI. Key requirements:
- 10 levels with increasing difficulty (speed + obstacles)
- Level jump from menu (start at any level 1-10)
- Resizable window with fixed game area
- Controls: Arrow keys OR WASD (selectable)
- No sound

## Solution

A local desktop snake game using Python's Tkinter library with:
- Main menu for Start and Level Select
- 10 difficulty levels with increasing speed and obstacles
- Keyboard control schemes (arrows or WASD)
- Resizable window, fixed game board

## User Stories

1. As a player, I want a main menu with Start button, so that I can begin playing
2. As a player, I want to jump to any level (1-10), so that I can test difficulty
3. As a player, I want to choose between Arrow keys and WASD controls, so that I can use my preferred scheme
4. As a player, I want the window to be resizable, so that it fits my screen
5. As a player, I want the game area to stay fixed size, so that gameplay is consistent
6. As a player, I want 10 levels with increasing speed, so that the game gets harder
7. As a player, I want obstacles that appear per level, so that I have more challenge
8. As a player, I want to see my current score, so that I know my progress
9. As a player, I want to see the current level, so that I know my progress
10. As a player, I want game over on collision, so that there is a lose condition
11. As a player, I want to grow the snake by eating food, so that I progress in the game
12. As a player, I want to control direction with arrow keys, so that I can play
13. As a player, I want to control direction with WASD, so that I can play
14. As a player, I want to see the snake rendered on screen, so that I can play
15. As a player, I want to see food rendered on screen, so that I know where to move
16. As a player, I want to see obstacles rendered on screen, so that I can avoid them
17. As a player, I want the snake to move automatically, so that gameplay is continuous
18. As a player, I want to control direction with keyboard, so that I can change course

## Implementation Decisions

**Modules:**
- `main.py` — Tkinter root window, app initialization
- `menu.py` — Main menu UI (Start button, Level Select, Control scheme)
- `game.py` — Game canvas, main loop, game state management
- `snake.py` — Snake entity (position, movement, growth, self-collision)
- `food.py` — Food entity (random placement, collision detection)
- `obstacle.py` — Obstacle entity (per-level generation, collision)
- `controls.py` — Input handling (key binding for arrows + WASD)
- `renderer.py` — Canvas rendering (snake, food, obstacles, score display)
- `game_loop.py` — Main game loop with tick timing

**Rendering System:**
- Snake drawn as connected rectangles (green segments)
- Food drawn as red square
- Obstacles drawn as gray/brown squares
- Score displayed as text on canvas
- Level displayed as text on canvas
- Grid uses cell_size=20 pixels per cell
- Canvas width/height = grid_width * cell_size, grid_height * cell_size
- **Grid boundary drawn as subtle grid lines (#222222)** so players can identify wall positions

**Main Game Loop:**
- Uses `root.after(tick_rate, callback)` for tick-based animation
- Each tick: move snake → check collisions → handle eat → render
- Initial tick rate: 150ms (level 1)
- Tick rate decreases with level (60ms at level 10)
- **Direction input is queued** - only one direction change per tick to prevent self-collision
- Rapid key presses before a tick are stored in `pending_direction` and applied on next tick

**Level Configuration:**
- Level 1: 150ms tick, 0 obstacles
- Level 2: 140ms tick, 2 obstacles
- Level 3: 130ms tick, 4 obstacles
- Level 4: 120ms tick, 6 obstacles
- Level 5: 110ms tick, 8 obstacles
- Level 6: 100ms tick, 10 obstacles
- Level 7: 90ms tick, 12 obstacles
- Level 8: 80ms tick, 14 obstacles
- Level 9: 70ms tick, 16 obstacles
- Level 10: 60ms tick, 18 obstacles

**Technical:**
- Grid: 20x20 cells (fixed), cell size adjusts to fit window
- Game states: MENU, PLAYING, GAME_OVER
- Snake starts at length 3
- Food respawns on eaten
- Obstacles placed randomly but not on snake start position

## Testing Decisions

Priority modules for tests:
- `snake.py` — movement, growth, self-collision
- `food.py` — spawn location not on snake
- `obstacle.py` — placement away from snake

Test external behavior only (not internal state).

## Out of Scope

- Sound/audio
- High scores / leaderboard
- Power-ups
- Multiple snake skins
- Network/multiplayer

## Further Notes

- Level jump starts at selected level, same starting snake size
- Controls selectable in menu, persists for game session
- Resizable window via Tkinter geometry manager (fixed canvas content)

## Enhancement #12 - Dynamic Grid Resizing

**Problem:** When the window is resized, the play area remains fixed (20x20 cells, 400x400 canvas), leaving black bars on the right and bottom. Players want the game area to fill the window.

**Solution:** The grid expands to fill the window. Cell size stays fixed at 20px. Grid width/height (in cells) adjusts based on window size. Minimum grid size is determined by window size at level start and level complete.

**User Stories:**

1. As a player, I want the play area to fill my window when I resize, so that I can use my full screen
2. As a player, I want the grid to expand in both directions (width and height), so that the play area fills the window fully
3. As a player, I want the minimum grid size to be set when I start a level, so that the minimum is based on my current window size
4. As a player, I want the minimum grid size to be updated when I resize on the level complete screen, so that the next level adapts to my window
5. As a player, I want resizing during gameplay to be deferred, so that the grid only resizes at safe moments (level start, level complete)
6. As a player, I want the minimum to reset when starting a new game from the menu, so that each session starts fresh
7. As a player, I want restarts within a level to keep the current minimum, so that I can retry without the grid changing
8. As a player, I want the HUD to stay visible and readable, so that I can always see score and level
9. As a player, I want the snake to start at a random position when the grid expands, so that gameplay feels fresh each level
10. As a player, I want grid resizing to have no maximum limit, so that large displays can use the full screen

**Implementation Decisions:**

**Grid Resizing:**
- `Grid` dataclass holds current `width` and `height` (in cells), plus fixed `cell_size=20`
- `Grid.canvas_width` and `Grid.canvas_height` derive from `width * cell_size` and `height * cell_size`
- Grid expands in width direction to fill window — cell count scales with window width
- No maximum grid size

**Resize Mechanism:**
- `<Configure>` event on root window records `target_canvas_width` — nothing else
- At the start of each `_game_loop()` tick, `_expand_grid_if_needed()` checks if `target_canvas_width` would produce a larger grid
- If larger, grid width is updated and canvas is resized
- Grid only expands, never shrinks

**Snake Start Position:**
- `Snake._reset()` spawns snake at a random position within valid grid cells, pointing LEFT
- `Obstacles.create` uses the current grid dimensions when spawning
- `Food.create` uses the current grid dimensions when spawning

**Rendering:**
- Canvas uses `fill=tk.BOTH, expand=True` — fills window in both dimensions
- HUD position stays fixed at pixel coordinates (10, 10) etc., not tied to grid
- `Renderer` reads canvas dimensions via `canvas.winfo_width()` each render

**Game States affected:**
- `MENU`: resize recorded but not applied
- `PLAYING`: resize deferred, applied at start of next tick via `_expand_grid_if_needed()`
- `GAME_OVER`: same as PLAYING (deferred via tick)
- `LEVEL_COMPLETE`: `_expand_grid_if_needed()` called in `_render_level_complete()`

**Out of Scope:**
- Shrinking the grid (grid only expands, never shrinks)
- Persisting window size across sessions
- Scaling the HUD (HUD stays same pixel size regardless of grid)
- Changing cell_size from 20

---

## Bug Fix #11 - Self-collision from rapid key presses

**Problem:** When player presses two direction keys quickly before a tick (e.g., DOWN then LEFT), the snake turns into its own body.

**Fix:** Implemented queued direction system in `snake.py`:
- `pending_direction` stores queued input
- Only one direction change processed per tick

## Enhancement #9 - Better collision feedback

**Problem:** Game shows generic "GAME OVER" without explaining why.

**Fix:** Display cause of death:
- "You hit the wall!"
- "You hit an obstacle!"
- "You hit yourself!"