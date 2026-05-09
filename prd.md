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

**Main Game Loop:**
- Uses `root.after(tick_rate, callback)` for tick-based animation
- Each tick: move snake → check collisions → handle eat → render
- Initial tick rate: 150ms (level 1)
- Tick rate decreases with level (60ms at level 10)

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