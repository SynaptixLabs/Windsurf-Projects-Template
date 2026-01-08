# Windsurf Projects Template (SynaptixLabs)

This repo is a **starter template** for bootstrapping (or upgrading) a SynaptixLabs-style Windsurf environment: **Rules + Roles + Agent tiers + Vibe Coding**.

Once you instantiate a real project repo, this README is meant to be replaced by the project's real `README.md`.

---

## What this template gives you

### 1) Vibe Coding Framework (`_global/`)
Global rules for **LLM-native development**:
- **Vibes** as the universal measure (1 Vibe = 1,000 tokens)
- Role identification (`[CTO]`, `[CPO]`, `[DEV:<module>]`, `[FOUNDER]`)
- GOOD/BAD/UGLY review protocol
- Quality gates (TDD, coverage targets)
- Sprint structure with Vibe budgets

### 2) Role "instances" you can invoke (Manual)
Concrete role prompts for **CTO** and **CPO** that you invoke with `@role_cto` / `@role_cpo`.

> These are *not* "the archetype of a CTO". They are the **operating prompt** for "the CTO agent in THIS repo".

### 3) Path-based routing (Glob)
Optional "editor glue" that reduces the "who am I?" problem by mapping **paths → default role**.

### 4) Tiered `AGENTS.md` (repo → domain → module)
Directory-scoped `AGENTS.md` are your **source of truth** for domain/module behavior and constraints:
- Root `AGENTS.md` (Tier-1)
- `backend/AGENTS.md`, `frontend/AGENTS.md` (Tier-2) — includes CLI auto-registration pattern
- Module-level `AGENTS.md` (Tier-3)

### 5) Reference Module (`backend/modules/_example/`)
A complete, copy-able module demonstrating:
- Standard structure (`src/`, `tests/`)
- CLI auto-registration pattern
- Service + model patterns
- Unit test examples

### 6) Documentation Templates (`docs/templates/`)
- `CHANGELOG_TEMPLATE.md` — Keep a Changelog format
- `SECURITY_TEMPLATE.md` — Security documentation
- `PRD_TEMPLATE.md` — Product requirements
- `DECISIONS_TEMPLATE.md` — ADR format

### 7) Core Documentation (`docs/`)
- `00_INDEX.md` — Entry point with reading order
- `01_ARCHITECTURE.md` — System architecture
- `02_SETUP.md` — Development setup
- `03_MODULES.md` — **Capability registry** (check before building!)
- `04_TESTING.md` — Testing strategy
- `05_DEPLOYMENT.md` — Deployment guide
- `ui/UI_KIT.md` — Design tokens, accessibility, component states

---

## How to use this template

### A) New project
1. Create a new GitHub repo from this template (or copy it).
2. Open the repo in Windsurf.
3. Configure rule activations (see below).
4. Replace this README with the project README once project initialization is complete.

### B) Upgrade an existing repo
1. Copy the relevant folders/files (typically `.windsurf/` + tiered `AGENTS.md` + `docs/` scaffolding you want).
2. Configure rule activations in Windsurf.
3. Merge your existing project README / docs with the template structure.

> Yes—"copy/paste rules to update existing ones" is a valid workflow. Treat this template as a **baseline** and sync forward when you improve it.

---

## Windsurf rules: what is GLOBAL vs LOCAL?

Windsurf supports **multiple rule "levels"**:

### Global rules (Windsurf-level, applies everywhere)
- Applies across **all workspaces** in your Windsurf installation.
- Good for personal defaults (tone, formatting, personal coding style).
- **Copy `_global/windsurf_global_rules.md` content to your Windsurf global rules.**

### Workspace rules (project-level, lives in the repo)
- Stored under `.windsurf/rules/` inside the repo.
- Applies only to that **project/workspace**.

### System rules (org/IT-level; enterprise style)
- Admin-managed rules that apply across machines/workspaces.
- Most teams will skip this unless they have a managed setup.

---

## Where rules live in the repo

```
.windsurf/
  rules/
    00_synaptix_ops.md
    01_artifact_paths.md
    02_templates_policy.md
    10_module_agent_permissions.md
    20_context_router.md
    role_cto.md
    role_cpo.md
  workflows/              (optional)
    ...your workflow .md files...
```

---

## Activation modes (Windsurf)

Each rule file has an **Activation Mode**:

- **Always On**: Always applied
- **Manual**: Activate by `@mention` (e.g., `@role_cto`)
- **Glob**: Auto-applies when editing files that match a path/glob
- **Model decision**: Let Cascade decide when to apply it

---

## Recommended activation mapping

### ✅ Always On
- `00_synaptix_ops`
- `10_module_agent_permissions` *(optional; otherwise Glob)*
- `01_artifact_paths`
- `02_templates_policy`

### 🎯 Glob
- `10_module_agent_permissions` → `backend/**`, `frontend/**`, `ml-ai-data/**`, `shared/**`
- `20_context_router` → `docs/**`, `backend/**`, `frontend/**`, `ml-ai-data/**`, `shared/**`

### 🧠 Manual
- `role_cto` → invoke with `@role_cto`
- `role_cpo` → invoke with `@role_cpo`

---

## Creating a new module

```bash
# Copy the reference module
cp -r backend/modules/_example backend/modules/your_module

# Update files:
# 1. README.md - module purpose
# 2. AGENTS.md - Tier-3 rules
# 3. src/*.py - your implementation
# 4. tests/ - your tests

# Register in docs/03_MODULES.md
```

---

## Vibe Quick Reference

| Task Type | Typical Vibes |
|-----------|---------------|
| Simple fix | 1–3 V |
| Single function + tests | 3–8 V |
| Module feature | 8–25 V |
| Cross-module work | 25–50 V |
| Sprint (small) | 50–150 V |
| Sprint (medium) | 150–300 V |

**1 Vibe = 1,000 tokens** (input + output combined)

---

## Fast checklist

- [ ] Open repo root as Windsurf workspace
- [ ] Copy `_global/windsurf_global_rules.md` to Windsurf global rules
- [ ] Set `00_synaptix_ops` → Always On
- [ ] Set `20_context_router` → Glob on docs + code paths
- [ ] Keep `role_cto` / `role_cpo` → Manual
- [ ] Replace this README when project is fully initialized

---

## Template Structure

```
Windsurf-Projects-Template/
├── _global/                    # Meta-rules (copy to Windsurf global)
│   └── windsurf_global_rules.md
├── .windsurf/rules/            # Workspace rules
├── AGENTS.md                   # Tier-1 (project-wide)
├── docs/
│   ├── 00_INDEX.md             # Entry point
│   ├── 03_MODULES.md           # Capability registry
│   ├── ui/UI_KIT.md            # Design system
│   └── templates/              # Doc templates
├── backend/
│   ├── AGENTS.md               # Tier-2 + CLI auto-registration
│   └── modules/_example/       # Reference implementation
├── frontend/
│   └── AGENTS.md               # Tier-2
├── shared/                     # Cross-cutting utilities
└── ml-ai-data/                 # ML/AI modules
```

---

*Last updated: 2025-01-08*
