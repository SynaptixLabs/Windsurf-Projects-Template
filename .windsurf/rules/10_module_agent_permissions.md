# 10 — Module Agent Permissions

Purpose: make module-agent autonomy explicit so they don’t stall or “ask permission” for routine repo work.
This is **horizontal horizontal policy**; it does not replace Tier‑2/Tier‑3 `AGENTS.md`.

## What module agents MAY do without asking
- Implement inside module scope per Tier‑3 `AGENTS.md`.
- Create/extend tests and refactors inside module scope.
- Update the following outside-module artifacts **when required by the work**:
  - `docs/sprints/**` (todo/report/DR/decisions)
  - `docs/0l_DECISIONS.md` (record decisions tied to their work)
  - `docs/03_MODULES.md` (only when module contracts/capabilities changed)
  - Root/module `README.md` (only when behavior/usage changed)

## What module agents MUST NOT do without escalation
Raise a **FLAG** and escalate to `[CTO]` (and `[FOUNDER]` if needed) before:
- Adding a new datastore/queue/search engine or changing persistence strategy.
- Introducing a new major framework/runtime to the repo.
- Changing a public cross-module contract (API, event schema, shared library exports).
- Weakening testing/observability/rollback posture for speed.
- Implementing capabilities owned by other modules (see `docs/03_MODULES.md`).

## If asked to work outside scope
If the request is outside your role or module scope:
- Do **not** start work.
- Raise a **FLAG** (GOOD/BAD/UGLY + recommendation) and ask for reroute/clarification.

## Output shape (module work)
When you finish a chunk of work, always provide:
- files touched/added
- change summary
- tests to run + current status
- next steps / risks
