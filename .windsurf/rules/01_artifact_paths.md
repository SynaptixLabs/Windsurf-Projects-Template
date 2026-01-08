# Common artifact paths (repo conventions)

## Always
- Global agent constitution (Tier‑1): `AGENTS.md`
- the editor ops rules: `.windsurf/rules/00_synaptix_ops.md`
- Global development standards: `_global/windsurf_global_rules.md`
- Docs index: `docs/00_INDEX.md`

## Tiers
- Tier‑2 domain agents:
  - `backend/AGENTS.md`
  - `frontend/AGENTS.md`
  - `ml-ai-data/AGENTS.md`
  - `shared/AGENTS.md`
- Tier‑3 module agents: `<domain>/<module>/AGENTS.md`

## Sprint system
- Sprint index: `docs/sprints/<SPRINT_ID>/<SPRINT_ID>_index.md`
- Sprint todos: `docs/sprints/<SPRINT_ID>/todo/`
- Sprint reports: `docs/sprints/<SPRINT_ID>/reports/`

## Templates
- Mandatory living docs templates: `docs/_templates/`
- Optional scaffolding templates/snippets: `templates/`

## SynaptixLabs “AGENTS” framework (when vendored/installed)
- CLI: `agents/slagents_cli/` (or your configured path)
- Testing harness / mocks: `agents/**` (see AGENTS project README)


## Decisions
- Primary decision log: `docs/0l_DECISIONS.md`
- ADRs (optional): `docs/adrs/ADR-*.md` (if used, also reference/link them from `docs/0l_DECISIONS.md`)
