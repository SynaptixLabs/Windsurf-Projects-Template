# /project:test — Run Full Test Suite

Run the full test suite for the current project. Check CLAUDE.md for project-specific commands.

## Steps

1. **Identify the project** from the current working directory.
2. **Check if a dev server is required** — see CLAUDE.md `Start the Server` section.
3. **Start the server if needed** and confirm it's running before E2E.
4. **Run tests in order:**
   - Unit tests first (fast feedback)
   - Integration tests (requires services)
   - E2E tests last (full system)
5. **Report results** with ✅/❌ per layer, counts, failures with file + line.

## Output format

```
## Test Run — [PROJECT] — [DATE]

Server: ✅ Running on port XXXX | ❌ Not running (E2E skipped)

### Unit Tests
Result: ✅ XX passed / ❌ XX failed
[failures if any]

### Integration Tests
Result: ✅ XX passed / ❌ XX failed

### E2E Tests
Result: ✅ XX passed / ❌ XX failed

### Overall Gate
[ ] PASS — safe to mark feature done
[ ] FAIL — do not mark done, see failures above
```

## Rules
- NEVER skip a layer without explicit Avi approval
- Server failure → report as test failure, do not proceed to E2E
- Save screenshots to `tests/screenshots/` for all GUI flows
