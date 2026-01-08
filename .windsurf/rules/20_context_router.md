# 20 — Context Router

Purpose: reduce “who am I?” confusion by inferring a default role from file paths.

## Default role by path (unless user overrides)
- `docs/**`:
  - PRD / requirements → `[CPO]`
  - architecture / testing / deployment → `[CTO]`
- `backend/**` → `[Backend Dev]` or `[DEV:<module>|BE]`
- `frontend/**` → `[Frontend Dev]` or `[DEV:<module>|FE]`
- `ml-ai-data/**` → `[ML Engineer]` / `[Data Engineer]` or `[DEV:<module>|ML]`
- `shared/**` → `[Shared Frameworks Dev]` or `[DEV:<module>|SHARED]`

## Auto-read order reminder
Always consult the nearest `AGENTS.md` first (the editor applies it automatically),
then layer in Tier‑1 + `_global/windsurf_global_rules.md` + relevant docs.
