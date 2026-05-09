# Domain Docs

Multi-context layout. Root file (`CONTEXT-MAP.md`) points to per-context `CONTEXT.md` files.

## Consumer Rules

- `CONTEXT-MAP.md` lives at repo root
- Each context has its own `CONTEXT.md` in a subdirectory (e.g., `frontend/CONTEXT.md`, `backend/CONTEXT.md`)
- Skills read `CONTEXT-MAP.md` first to find the relevant context file
- ADRs live in `docs/adr/` at repo root (shared across all contexts)

## To Add a Context

1. Create `CONTEXT.md` in the new subdirectory
2. Add entry to `CONTEXT-MAP.md`