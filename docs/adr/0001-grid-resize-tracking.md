# ADR 0001: Dual-Width-Height Resize Tracking Pattern

**Date:** 2026-05-10
**Status:** Accepted

## Context

When implementing Enhancement #12 (dynamic grid resizing), an initial simplification tracked only `target_canvas_width`, ignoring window height changes. This caused Bug #15 where resizing the window taller left `grid.height` stale, mispositioning walls.

## Decision

Track **both** `target_canvas_width` and `target_canvas_height` independently:

```python
self.target_canvas_width = 400
self.target_canvas_height = 400

def _on_resize(self, event):
    if event.width == 1 and event.height == 1:
        return
    self.target_canvas_width = event.width
    self.target_canvas_height = event.height

def _expand_grid_if_needed(self):
    new_width = self.target_canvas_width // self.grid.cell_size
    new_height = self.target_canvas_height // self.grid.cell_size
    if new_width > self.grid.width:
        self.grid.width = new_width
        self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)
    elif new_width < self.grid.width and new_width >= 20:
        self.grid.width = new_width
        self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)
    if new_height > self.grid.height:
        self.grid.height = new_height
        self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)
    elif new_height < self.grid.height and new_height >= 20:
        self.grid.height = new_height
        self.canvas.config(width=self.grid.canvas_width, height=self.grid.canvas_height)
```

## Consequences

**Positive:**
- Grid adapts to window resizing in **both dimensions independently**
- Avoids regression where height changes are silently ignored
- Clear separation: resize event only records targets, expansion logic applies them

**Negative:**
- Two variables instead of one — slightly more cognitive overhead
- `_expand_grid_if_needed()` must handle both width and height branches

## Alternatives Considered

1. **Single `target_canvas_width` only** — rejected; causes height staleness bug (#15)
2. **Tuple `(target_width, target_height)`** — equivalent but less readable in attribute access
3. **Resize event directly modifies grid** — rejected; violates deferred resize principle (resizes only at safe moments)

## Notes

- The `if event.width == 1 and event.height == 1: return` guard filters spurious Configure events from Tkinter initialization
- Minimum grid size enforced at 20 cells per dimension to keep gameplay playable
- `_expand_grid_if_needed()` called at: level start, each game loop tick, level complete render, and menu show (Bug Fix #16)