# /project:regression — Full Regression Gate

Run before any merge or "done" declaration. Uses commands from CLAUDE.md.

## Steps

1. Run full unit + integration + E2E test suite
2. Check for regressions vs last known passing state
3. Run E2E smoke on critical paths
4. Static checks (TypeScript / mypy / ruff)
5. Security scan for secrets

## Regression Gate Checklist

```
[ ] All unit tests pass
[ ] All integration tests pass
[ ] E2E smoke on critical paths pass
[ ] No type errors (npm run type-check / mypy)
[ ] No lint errors
[ ] No hardcoded secrets (git grep -i "api_key\|secret\|password")
[ ] No .env files staged (git status check)
[ ] Docs updated if architecture changed
[ ] Avi sign-off
```

## Output

- **PASS**: print full ✅ checklist
- **FAIL**: list every failing item with file + line — do not mark done
