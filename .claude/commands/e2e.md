# /project:e2e — E2E Browser Testing with Playwright MCP

Run end-to-end browser tests using the Playwright MCP tool against the running dev server.

## Steps

1. **Verify dev server is running** — check CLAUDE.md for port + start command.
2. **If not running** → start it and wait for "ready" before proceeding.
3. **Navigate to the app** using Playwright MCP.
4. **Run critical user flows** from CLAUDE.md `Common Flows to Test` section.
5. **Screenshot every significant state** → save to `tests/screenshots/e2e_[timestamp]/`
6. **Report pass/fail per flow.**

## Playwright MCP Pattern

```
- playwright_navigate  → go to page
- playwright_screenshot → after every major action (REQUIRED)
- playwright_click, playwright_fill → for interactions
- NEVER assume success — always screenshot to verify
```

## Rules

- Real running server required — no mocks for E2E
- Every assertion must have a screenshot
- On step failure → screenshot the failure state + stop + report
- Test with realistic-looking data (not "test123")

## Output format

```
## E2E Run — [PROJECT] — [DATE]

Server: ✅ http://localhost:XXXX

### Flow: [Flow Name]
Step 1: [action] → ✅ tests/screenshots/001_name.png
Step 2: [action] → ❌ FAILED: [reason] → tests/screenshots/002_error.png

### Summary
Flows passed: X/Y
Critical failures: [list]

Gate: [ ] PASS | [ ] FAIL
```
