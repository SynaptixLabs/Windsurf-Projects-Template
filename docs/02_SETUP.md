# {{PROJECT_NAME}} — Setup Guide

> **Development Environment Setup**  
> Owner: CTO

---

## Prerequisites

| Tool | Version | Required |
|------|---------|----------|
| {{LANG_RUNTIME}} | {{VERSION}} | ✅ |
| {{PACKAGE_MANAGER}} | {{VERSION}} | ✅ |
| Docker | Latest | Optional |
| Git | Latest | ✅ |

---

## Quick Setup

```bash
# 1. Clone repository
git clone {{REPO_URL}}
cd {{PROJECT_NAME}}

# 2. Install dependencies
{{INSTALL_COMMAND}}

# 3. Environment setup
cp .env.example .env
# Edit .env with your values

# 4. Database setup
{{DB_SETUP_COMMAND}}

# 5. Verify installation
{{VERIFY_COMMAND}}
```

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Database connection | ✅ | - |
| `SECRET_KEY` | App secret | ✅ | - |
| `DEBUG` | Debug mode | ❌ | `false` |
| `LOG_LEVEL` | Logging level | ❌ | `INFO` |

---

## Running the Application

### Development Mode
```bash
{{DEV_RUN_COMMAND}}
```

### Production Mode
```bash
{{PROD_RUN_COMMAND}}
```

### With Docker
```bash
docker-compose up -d
```

---

## Running Tests

```bash
# All tests
{{TEST_ALL_COMMAND}}

# Unit tests only
{{TEST_UNIT_COMMAND}}

# With coverage
{{TEST_COVERAGE_COMMAND}}
```

---

## IDE Setup

### VS Code
Recommended extensions:
- {{EXTENSION_1}}
- {{EXTENSION_2}}
- {{EXTENSION_3}}

### Windsurf
See `AGENTS.md` files for agent-specific configurations.

---

## Troubleshooting

### Common Issues

**Issue:** {{COMMON_ISSUE_1}}
```bash
# Solution
{{SOLUTION_1}}
```

**Issue:** {{COMMON_ISSUE_2}}
```bash
# Solution
{{SOLUTION_2}}
```

---

## Vibe Cost

| Setup Task | Vibes |
|------------|-------|
| Fresh setup | 2–3 V |
| Dependency update | 1–2 V |
| Environment debug | 3–5 V |

---

*Last updated: {{DATE}}*
