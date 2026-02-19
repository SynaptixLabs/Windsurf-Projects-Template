# /project:release-gate — Pre-Release Checklist

Run before any production deployment or public demo.

## Gate Checklist

### Code Quality
```
[ ] All tests pass (unit + integration + E2E)
[ ] No regressions vs previous release
[ ] Type errors: NONE
[ ] Lint: CLEAN
[ ] Coverage meets minimum threshold
```

### Security
```
[ ] No hardcoded secrets
[ ] .env files not committed
[ ] Dependencies audited (npm audit / pip-audit)
[ ] Auth flows tested
[ ] Rate limiting in place (if public-facing)
```

### Infrastructure
```
[ ] Environment variables set in prod
[ ] Database migrations applied
[ ] Health endpoint responding
[ ] Rollback plan defined
```

### Documentation
```
[ ] CHANGELOG.md updated
[ ] README accurate
[ ] CLAUDE.md reflects current architecture
[ ] docs/03_MODULES.md current
```

### Demo Readiness
```
[ ] Demo script written and tested
[ ] Test data seeded (if needed)
[ ] No debug logs in output
[ ] Build succeeds cleanly
```

## Final Sign-off

**Avi must explicitly approve before proceeding to production.**

Output: Full ✅/❌ checklist + blockers list + GO / NO-GO recommendation.
