# Agent Brief - Snake Game

## Current State

Fully playable Snake game with 10 levels. Run with `python3 game.py`.

## Completed Issues

| # | Issue | Status |
|----|-------|--------|
| #1 | PRD - Snake Game with 10 Levels |
| #2 | Basic Window + Canvas |
| #3 | Snake + Movement |
| #4 | Food + Eating |
| #5 | Collision + Game Over |
| #6 | Main Menu |
| #7 | Levels + Obstacles |
| #8 | Rendering + Game Loop |
| #9 | Game ends abruptly (new - needs work) |
| #10 | Level progression (implemented, not fully tested) |

## Known Issues

### #9 - Game ends abruptly without feedback
- **Problem:** Players die without understanding why
- **Status:** Needs work
- **Suggestion:** Add visual feedback when hitting wall/obstacle

### #10 - Level progression
- **Status:** Implemented but needs testing
- **Fix in:** commit 5f2f9d0

## Level Config

```python
LEVEL_CONFIG = {
    1: {"tick": 150, "obstacles": 0, "goal": 50},
    2: {"tick": 140, "obstacles": 2, "goal": 60},
    ...
    10: {"tick": 60, "obstacles": 18, "goal": 140},
}
```

## Controls

- Arrow keys OR WASD (selectable in menu)
- R to restart after game over / level complete

## Key Files

- `game.py` - Main game class
- `snake.py` - Snake entity
- `food.py` - Food entity
- `obstacles.py` - Obstacles
- `renderer.py` - Canvas rendering
- `menu.py` - Main menu UI
- `controls.py` - Input mapping

## Triage Labels

- `needs-triage` - needs evaluation
- `needs-info` - waiting on reporter
- `ready-for-agent` - AFK-ready
- `ready-for-human` - needs human

## Next Steps

1. Test level progression (issue #10)
2. Add better collision feedback (issue #9)
3. Consider obstacle visibility (they may blend with background)