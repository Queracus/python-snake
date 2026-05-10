# ADR 0001: Grid Resize Tracking Both Width and Height

## Status

Accepted

## Context

When the game window is resized, the grid needs to expand to fill the available space. A regression was introduced when the grid resize logic was simplified to only track `target_canvas_width`, ignoring height changes entirely.

This caused walls to remain at incorrect positions when the window was resized taller, because the grid height was never updated to match the new window dimensions.

## Decision

We will track both `target_canvas_width` AND `target_canvas_height` during resize events:

1. **Game class** will maintain two target variables:
   - `target_canvas_width` - the target canvas width from resize events
   - `target_canvas_height` - the target canvas height from resize events

2. **`_on_resize()` method** will update both variables:
   ```python
   self.target_canvas_width = event.width
   self.target_canvas_height = event.height
   ```

3. **`_expand_grid_if_needed()` method** will expand grid in both dimensions:
   - Expand grid width when window gets wider
   - Expand grid height when window gets taller
   - Contract grid in either dimension if window shrinks (minimum 20 cells)

4. **`show_menu()` method** will reset both dimensions to default (400x400)

## Consequences

### Positive

- Grid correctly expands in both dimensions when window is resized
- Walls render at correct positions (window edges)
- Consistent behavior for width and height

### Negative

- Slightly more code to maintain (two variables instead of one)

## Related Issues

- GitHub Issue #15: Bug: Grid height not tracked during resize causing wall mispositioning