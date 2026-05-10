## Problem Statement

Currently, when a player completes a level in snake game, the game pauses and waits for the player to press 'R' to proceed to the next level. This creates unnecessary friction. Additionally, the snake spawns too close to walls (only 1-2 cells away), which gives players insufficient reaction time when the snake immediately moves toward a wall.

## Solution

Implement automatic level transitions with a countdown timer and improve snake spawn positioning to give players adequate reaction time.

## User Stories

1. As a player, I want the game to automatically start the next level after a countdown so I don't have to press any key to continue.
2. As a player, I want to see a countdown timer on the screen during level transition so I know when the next level will start.
3. As a player, I want the snake to spawn at least 7 cells away from any wall so I have time to react if the snake moves toward a wall.
4. As a player, I want the game to return to the menu after completing level 10 with a countdown so the transition feels natural.
5. As a player, I want the minimum window size to be 20x20 cells so the game is always playable.

## Implementation Decisions

- **Game class modifications**: Modify `Game` class to handle automatic level transitions with countdown. Add `countdown` state and `countdown_remaining` attribute.
- **Spawn logic in Snake class**: Update `_reset()` method to spawn snake head at least 7 cells from any wall boundary.
- **Grid minimum enforcement**: Ensure grid dimensions cannot go below 20x20 in the resize handler.
- **Renderer updates**: Add countdown display during level transition (shows "Next level in X..." with remaining seconds).
- **State machine update**: Add a `COUNTDOWN` state between `LEVEL_COMPLETE` and transitioning to next level or menu.
- **Timing**: 4-second countdown for all level transitions, including after level 10.

### Modules to Modify

1. `game.py` - Add countdown logic and state handling
2. `snake.py` - Update spawn position logic
3. `renderer.py` - Add countdown display
4. `game.py` - Add minimum grid size enforcement in resize handler

## Testing Decisions

- Test snake spawn position is at least 7 cells from all four walls
- Test countdown timer displays and decrements correctly
- Test auto-transition to next level after countdown completes
- Test auto-transition to menu after level 10 countdown
- Test minimum grid size of 20 is enforced
- Existing test files in `tests/` follow similar patterns for state machine and rendering tests

## Out of Scope

- Adding sound effects during countdown
- Custom countdown durations per level
- Visual themes for countdown display

## Further Notes

The implementation should maintain backward compatibility with existing controls and menu system.