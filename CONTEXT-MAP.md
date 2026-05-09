# CONTEXT-MAP

Multi-context layout for this repo. Each context is a functional area with its own domain language.

## Contexts

| Name | Path | Description |
|------|------|-------------|
| core | `core/` | Core game logic (snake, food, grid) |

---

## Adding a New Context

1. Create a subdirectory (e.g., `frontend/`, `api/`)
2. Add a `CONTEXT.md` file in that subdirectory
3. Add an entry to the table above

Example:
```markdown
| frontend | `frontend/` | UI layer |
```

## Reading the Map

Skills read this file to find the relevant context. When working on a feature:

- If it relates to core game logic → use `core/CONTEXT.md`
- If it adds a new area → create new context + add entry here