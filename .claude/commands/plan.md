# /project:plan — Force Plan Mode for Complex Tasks

Invoke BEFORE starting any task that touches >2 files, crosses module boundaries, or involves user-facing flow changes.

## Produce this plan before writing any code

```
## Task: [description]

### Impact assessment
Files to touch: [list with paths]
Modules affected: [list]
Cross-boundary changes: YES/NO — [explain if yes]
One-way doors: YES/NO — [list if yes]
New dependencies: YES/NO — [FLAG to CTO if yes]

### Approach
Step 1: [action] → [file]
Step 2: [action] → [file]
Step 3: [action] → [file]

### Test plan
- Unit: [what to test]
- Integration: [what to test]
- E2E: [user flows to verify]

### Risks / assumptions
- [risk 1]
- [assumption 1]

### Scope
In scope: [explicit list]
Out of scope: [explicit list]

### Vibe estimate
~X Vibes (1 Vibe = 1K tokens)
```

## After producing the plan

**STOP. Wait for Avi approval before executing.**

Only proceed after: "go", "approved", "proceed", or equivalent.
