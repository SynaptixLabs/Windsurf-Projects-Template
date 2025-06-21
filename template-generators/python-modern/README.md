# Python Modern Template Generator (2025)

A comprehensive, generic Python project template using modern 2025 tooling and best practices. This template serves as the foundation for all Python project types.

## Features

### Modern 2025 Python Stack
- **Python 3.11-3.13** support
- **Ruff** - Universal linter + formatter (10-100x faster than alternatives)
- **MyPy** - Strict type checking
- **Poetry/UV** - Dependency management (UV is 80x faster than pip)
- **pytest** - Comprehensive testing framework
- **Pydantic v2** - Data validation and settings
- **Structured logging** with structlog

### Project Types Supported
- **Web API** - FastAPI with async/await
- **Agentic AI** - CrewAI multi-agent systems
- **Data Science** - Polars + DuckDB + Prefect/Airflow
- **Game Development** - Pygame for 2D games
- **CLI Tool** - Typer-based command line applications
- **Library** - Reusable Python packages

### Advanced Features
- **Database Integration** - PostgreSQL, MongoDB, Redis, ChromaDB, Pinecone
- **Testing Levels** - Basic, Comprehensive, Enterprise
- **CI/CD** - GitHub Actions with matrix testing
- **Docker** - Multi-stage builds for production
- **Documentation** - Sphinx/MkDocs with auto-generation
- **Windsurf IDE Integration** - AI-assisted development

### Quality & Performance
- **Test Coverage** - Configurable thresholds (default 85%)
- **Security Scanning** - Bandit + Safety for enterprise
- **Performance Testing** - pytest-benchmark + Locust
- **Property-based Testing** - Hypothesis for complex validation
- **Parallel Testing** - pytest-xdist for faster execution

## Quick Start

### Prerequisites
- [Copier](https://copier.readthedocs.io/) - `pip install copier`
- Python 3.11+ 
- Git

### Generate a New Project

```bash
# Generate project with interactive prompts
copier copy path/to/python-modern my-new-project

# Use specific template version
copier copy path/to/python-modern@v1.2.0 my-project

# Update existing project
cd my-existing-project
copier update
```

### Interactive Configuration

The template will prompt you for:

1. **Basic Information**
   - Project name and description
   - Author details

2. **Technical Stack**
   - Python version (3.11, 3.12, 3.13)
   - Project type (web-api, agentic-ai, data-science, etc.)
   - Package manager (Poetry or UV)

3. **Database Integration**
   - PostgreSQL, MongoDB, Redis
   - Vector databases (ChromaDB, Pinecone)

4. **Development Features**
   - Testing level (basic, comprehensive, enterprise)
   - Documentation style (Sphinx or MkDocs)
   - CI/CD integration
   - Docker configuration
   - Windsurf IDE integration

5. **Type-Specific Options**
   - **Agentic AI**: CrewAI features (agents, flows, tools, memory)
   - **Web API**: Authentication, API versioning
   - **Data Science**: Orchestration tools, Jupyter notebooks
   - **Game Development**: Game type, asset inclusion

## Generated Project Structure

```
my-project/
├── src/my_project/              # Source code (src layout)
│   ├── core/                    # Core business logic
│   ├── models/                  # Pydantic data models
│   ├── api/                     # FastAPI routes (web-api/agentic-ai)
│   ├── agents/                  # CrewAI agents (agentic-ai)
│   ├── data/                    # Data processing (data-science)
│   ├── game/                    # Game logic (game-development)
│   ├── utils/                   # Utility functions
│   └── main.py                  # Entry point
├── tests/                       # Comprehensive test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── performance/             # Performance benchmarks
├── scripts/                     # CLI automation scripts
├── docs/                        # Documentation
│   ├── projectRoadmap.md        # Windsurf integration
│   ├── currentStatus.md         # Development status
│   └── techStack.md             # Technology decisions
├── .github/workflows/           # CI/CD pipelines
├── pyproject.toml              # Single source of truth
├── .windsurfrules              # Windsurf AI customization
├── .windsurf_config.yaml       # Windsurf team settings
└── README.md                   # Project documentation
```

## Key Template Improvements

### Fixed Issues
- ✅ **Poetry Scripts** - Proper Python function references (not shell commands)
- ✅ **Modern Linting** - Ruff replaces Black, isort, flake8 (30x faster)
- ✅ **Type Safety** - MyPy strict mode with comprehensive coverage
- ✅ **Testing** - Parallel execution, property-based testing, containers

### 2025 Best Practices
- ✅ **Src Layout** - Industry standard project structure
- ✅ **Conditional Generation** - Only create files you need
- ✅ **Template Updates** - Copier migration support
- ✅ **AI Integration** - Windsurf IDE configuration included

### Performance Optimizations
- ✅ **Rust-powered Tools** - 10-100x speedups with Ruff
- ✅ **Parallel Processing** - Multi-core testing and linting
- ✅ **Efficient Dependencies** - UV option for 80x faster installs
- ✅ **Docker Multi-stage** - Minimal production images

## Advanced Usage

### Template Customization

The template supports extensive customization through Jinja2 templating:

```yaml
# Custom values in copier.yml
databases: ["postgresql", "redis", "chromadb"]
testing_framework: "enterprise"
include_auth: true
crewai_features: ["basic-agents", "flows", "memory"]
```

### CI/CD Integration

Generated projects include:
- **Matrix Testing** - Multiple Python versions
- **Security Scanning** - Automated vulnerability detection
- **Performance Monitoring** - Regression detection
- **Docker Building** - Automated container deployment

### Development Workflow

```bash
# Development commands (auto-generated)
poetry run dev          # Development mode with auto-reload
poetry run test         # Run test suite with coverage
poetry run lint         # Code quality checks
poetry run ci           # Full CI pipeline locally
poetry run format       # Auto-format code
poetry run clean        # Clean build artifacts
```

## Template Inheritance

This base template can be extended for specific use cases:

1. **python-game-development** - Adds Pygame, performance profiling
2. **python-agentic-ai** - Adds CrewAI, vector databases, agent templates
3. **python-data-science** - Adds Polars, DuckDB, workflow orchestration

## Contributing

1. Fork the template repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Test with multiple project types
4. Ensure Copier validation passes
5. Submit Pull Request

### Testing Templates

```bash
# Test template generation
copier copy . test-project --data project_type=web-api

# Test template updates
cd test-project
copier update --conflict=inline

# Validate generated project
cd test-project && poetry install && poetry run ci
```

## Version History

- **v1.2.0** - Added UV package manager support
- **v1.1.0** - Ruff formatter, removed Black dependency  
- **v1.0.0** - Initial modern Python template

## License

MIT License - Build amazing Python projects with modern tooling!
