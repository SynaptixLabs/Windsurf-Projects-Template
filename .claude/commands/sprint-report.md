# /project:sprint-report — Generate Sprint Status Report

Produce a concise sprint status report. Read sprint docs from `docs/sprints/`.

## Steps

1. Read the current sprint index (`docs/sprints/sprint_XX/sprint_XX_index.md`)
2. Read all module todo + report files in the sprint folder
3. Check test status from recent runs

## Output Format

```
## Sprint [XX] Status Report — [PROJECT] — [DATE]

### ✅ Done (shipped + tested)
- [item]

### 🔄 In Progress
- [item] — [module] — ETA: [estimate]

### ❌ Blocked
- [item] — Blocked by: [reason] — Needs: [what]

### 🎯 Sprint Goal
[one sentence — will we hit it?]
Status: ON TRACK / AT RISK / MISSED

### Quality Gates
Tests passing: YES/NO
Regressions: NONE / [list]
Demo-ready: YES / NO — [what's missing]

### CTO Pre-Release Verification
[ ] Code integrity
[ ] Tests pass + coverage
[ ] Environment verified
[ ] Docs updated
[ ] Architecture compliance
[ ] Security review

### Next Actions (top 3)
1. [action] — [role]
2. [action] — [role]
3. [action] — [role]
```
