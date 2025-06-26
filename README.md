# Windsurf Projects Template Generator v5.0 "Robustus"

Production-ready Python project template generator optimized for Windsurf IDE with state-of-the-art tooling and template inheritance.

## 🎯 Current Status

**✅ Production Ready:**
- **python-game-development** - Complete game development template with Pygame
- **python-modern** - Base template for all projects
- **Template Inheritance System** - Proven, working pattern
- **Windsurf IDE Integration** - Complete AI-powered development workflow  
- **Git/GitHub Automation** - Repository creation and auto-commit
- **Sprint-Based Development** - TODO generation and project management

**🔄 In Development (Structure Ready):**
- **agentic-ai** - crew.ai + FastAPI + Vector DBs (coming soon)
- **data-science** - Polars + Prefect + DuckDB (coming soon)
- **web-api** - FastAPI + SQLAlchemy (coming soon)
- **agentic-medallion** - Multi-layer data architecture (coming soon)
- **custom-multi** - Configurable template combinations (coming soon)

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** 
- **Windsurf IDE**
- **Git** and **GitHub CLI** (optional, for auto-commit)

### Generate a New Project

```bash
# Navigate to your projects directory
cd C:\Synaptix-Labs\projects

# Create and enter new project directory
mkdir my-awesome-game
cd my-awesome-game

# Generate project (interactive)
python C:\Synaptix-Labs\projects\Windsurf-Projects-Template\scripts\windsurf_generator.py python-game-development --interactive
```

**That's it!** Your project will be generated with:
- ✅ Complete Python package structure
- ✅ Pygame game development setup
- ✅ Testing infrastructure (pytest + Hypothesis)
- ✅ Code quality tools (Ruff + MyPy + pre-commit)
- ✅ GitHub repository (optional, with auto-commit)
- ✅ Sprint-based TODO lists for development
- ✅ Windsurf AI configuration

## 📁 Available Templates

### 🎮 **python-game-development** ✅ Production Ready
**Extends:** `python-modern`
- **Stack:** Python 3.12 + Pygame + Poetry + Ruff + MyPy
- **Use Cases:** 2D games, board games, AI opponents, arcade games
- **Features:** 
  - Game engine foundation with config system
  - Comprehensive testing (unit + integration + performance)
  - Sprint-based development workflow
  - Windsurf AI integration for guided development
  - GitHub automation with auto-commit

### 🏗️ **python-modern** ✅ Production Ready (Base Template)
- **Stack:** Python 3.12 + Poetry + FastAPI + Pydantic v2
- **Use Cases:** Base for all other templates
- **Features:** Modern Python project foundation

### 🤖 **agentic-ai** 🔄 Coming Soon
**Extends:** `python-modern`
- **Stack:** crew.ai + FastAPI + Pydantic v2 + Vector DBs
- **Use Cases:** Multi-agent systems, intelligent automation, RAG applications
- **Features:** Agent orchestration, tool integration, async processing
- **Status:** Template structure ready, implementation in progress

### 📊 **data-science** 🔄 Coming Soon
**Extends:** `python-modern`
- **Stack:** Polars + Prefect + Jupyter + DuckDB
- **Use Cases:** ETL pipelines, analytics, ML workflows
- **Features:** Fast data processing, workflow orchestration, notebooks
- **Status:** Template structure ready, implementation in progress

### 🌐 **web-api** 🔄 Coming Soon
**Extends:** `python-modern`
- **Stack:** FastAPI + SQLAlchemy + Pydantic v2
- **Use Cases:** REST APIs, microservices, backend services
- **Features:** Async endpoints, database integration, API documentation
- **Status:** Template structure ready, implementation in progress

### 🏗️ **agentic-medallion** 🔄 Coming Soon
**Extends:** `agentic-ai`
- **Stack:** crew.ai + Prefect + Multi-DB (Bronze→Silver→Gold)
- **Use Cases:** Data lakes, intelligent data processing, enterprise data platforms
- **Features:** Layered data architecture, AI-driven processing, multi-source integration
- **Status:** Template structure ready, implementation in progress

### 🔧 **custom-multi** 🔄 Coming Soon
- **Stack:** Configurable combination of above templates
- **Use Cases:** Complex projects requiring multiple paradigms
- **Features:** Template composition, shared components, unified configuration
- **Status:** Template structure ready, implementation in progress

## 🛠️ Technology Stack

**Core Stack:**
- **Python 3.12** - Latest stable Python
- **Poetry** - Modern dependency management
- **Ruff** - Ultra-fast Python linter (replaces Flake8, Black, isort)
- **MyPy** - Static type checking
- **pytest + Hypothesis** - Testing framework with property-based testing

**Development Tools:**
- **Windsurf IDE** integration with project-specific `.windsurfrules`
- **Pre-commit hooks** for automated code quality
- **GitHub Actions** for CI/CD
- **Docker** containerization ready
- **VCR.py** for HTTP interaction testing

**Game Development (python-game-development):**
- **Pygame** - 2D game development
- **Game engine architecture** - Modular, testable design
- **Performance profiling** - Built-in performance monitoring
- **AI algorithms** - Foundation for game AI implementation

## 🎯 Key Features

### Template Inheritance System
```
python-modern (Base)
    ↓ inherits & extends
python-game-development (Specialized) ✅ Ready
    ↓ 
agentic-ai (Specialized) 🔄 Coming Soon
    ↓
agentic-medallion (Super-Specialized) 🔄 Coming Soon
```
- **Shared foundation** - Common Python project structure
- **Specialized extensions** - Domain-specific features and configurations
- **Consistent quality** - All templates follow same standards
- **Proven pattern** - Successfully demonstrated with game development template

### Windsurf AI Integration
- **Project-specific `.windsurfrules`** - AI understands your project context
- **Sprint-based TODO generation** - Structured development workflow
- **Guided development** - AI helps with implementation decisions
- **Context-aware assistance** - Based on your project's architecture

### Sprint-Based Development
- **Sprint 1:** Infrastructure setup (Poetry, testing, CI/CD)
- **Sprint 2:** Core implementation (domain-specific logic)
- **Sprint 3:** Advanced features (AI, optimization, integrations)
- **Sprint 4:** Polish and optimization (performance, documentation)

### GitHub Integration
- **Automatic repository creation** - Via GitHub CLI or API
- **Auto-commit** - Initial project setup committed automatically
- **CI/CD workflows** - GitHub Actions for testing and deployment
- **Security scanning** - Automated vulnerability detection

## 📚 Generated Project Structure

```
my-awesome-game/
├── src/my_awesome_game/         # Main source code
│   ├── core/                    # Game engine core
│   ├── game/                    # Game logic
│   ├── ui/                      # User interface
│   └── config/                  # Configuration management
├── tests/                       # Comprehensive test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── conftest.py              # pytest configuration
├── docs/                        # Documentation & TODOs
│   ├── TODO.my-awesome-game.1.md # Sprint 1 tasks
│   ├── TODO.my-awesome-game.2.md # Sprint 2 tasks
│   ├── TODO.my-awesome-game.3.md # Sprint 3 tasks
│   └── TODO.my-awesome-game.4.md # Sprint 4 tasks
├── scripts/                     # Utility scripts
├── logs/                        # Application logs
├── .windsurfrules              # Windsurf AI configuration
├── .github/workflows/           # CI/CD pipelines
├── pyproject.toml              # Project configuration
├── pytest.ini                 # Test configuration
├── Dockerfile                  # Container configuration
└── README.md                   # Project documentation
```

## 🎮 Game Development Workflow (Current)

### 1. Generate Project
```bash
python scripts/windsurf_generator.py python-game-development --interactive
```

### 2. Open in Windsurf
- File → Open Folder → Select your project directory
- Windsurf reads `.windsurfrules` and understands your project context

### 3. Follow Sprint TODOs
- **Sprint 1:** `docs/TODO.your-game.1.md` - Set up development environment
- **Sprint 2:** `docs/TODO.your-game.2.md` - Implement core game mechanics
- **Sprint 3:** `docs/TODO.your-game.3.md` - Add advanced features
- **Sprint 4:** `docs/TODO.your-game.4.md` - Polish and optimize

### 4. AI-Assisted Development
Ask Windsurf:
- *"Help me implement the game logic for my space invaders game"*
- *"Review my collision detection code and suggest improvements"*
- *"Create unit tests for my player movement system"*
- *"Optimize this game loop for better performance"*

## 🔧 Advanced Usage

### Non-Interactive Generation
```bash
python scripts/windsurf_generator.py python-game-development \
  --project-name "space-invaders" \
  --author-name "Your Name" \
  --github-org "YourOrg" \
  --private
```

### Check Dependencies
```bash
python scripts/util_check_dependencies.py
```

### Validate Generated Project
```bash
python scripts/lib_project_validator.py /path/to/your/project
```

## 🎯 Development Philosophy

**You are the Product Manager.** The template generator provides:
- **Solid foundation** - Production-ready project structure
- **Flexible architecture** - Extend and customize as needed
- **AI guidance** - Windsurf helps with implementation
- **Best practices** - Modern Python development standards

## 🔄 Template Development Roadmap

### Current (v5.0 "Robustus")
- ✅ Template inheritance system (proven with game development)
- ✅ Game development templates (production ready)
- ✅ Git/GitHub automation (working)
- ✅ Windsurf AI integration (complete)
- ✅ Template structure for future expansions (ready)

### Immediate Next (v5.1) - In Active Development
- 🔄 **agentic-ai** - crew.ai + FastAPI + Vector DBs
- 🔄 **data-science** - Polars + Prefect + DuckDB  
- 🔄 **web-api** - FastAPI + SQLAlchemy + async

### Soon (v5.2)
- 🔄 **agentic-medallion** - Multi-layer data architecture
- 🔄 **custom-multi** - Template composition system

### Future (v6.0)
- 🔄 **Template marketplace** - Community templates
- 🔄 **Visual template builder** - GUI for template creation
- 🔄 **Cloud deployment** - One-click deployment to various platforms

## 🤝 Contributing

Interested in helping with template development?

**Immediate Opportunities:**
- Help implement the **agentic-ai** template (crew.ai expertise needed)
- Contribute to **data-science** template (Polars/Prefect experience helpful)
- Enhance **web-api** template (FastAPI/SQLAlchemy knowledge valuable)

**Process:**
1. **Fork** the repository
2. **Choose** a template in development from `template-generators/`
3. **Follow** the inheritance pattern from `python-modern`
4. **Test** thoroughly with the validator
5. **Submit** a pull request

## 📖 Documentation

- **Architecture:** `scripts/ARCHITECTURE_v4.md`
- **Template Inheritance:** `README_INHERITANCE.md`
- **Usage Guide:** `USAGE.md`
- **Windsurf Integration:** `docs/windsurf-integration-guide.md`

## 🚀 Quick Commands

```bash
# Generate new game project (working now)
python scripts/windsurf_generator.py python-game-development --interactive

# Generate base project (working now)
python scripts/windsurf_generator.py python-modern --interactive

# Check system ready
python scripts/git_validator.py

# Validate generated project
python scripts/lib_project_validator.py /path/to/project

# See available templates (including coming soon)
python scripts/windsurf_generator.py --list-templates
```

---

**🎮 Ready to build your next Python project with AI-powered development!**

Start with the `python-game-development` template for immediate use, or help us complete the other templates for the broader Python ecosystem.

---

*Windsurf Projects Template Generator v5.0 "Robustus" - Production-ready foundation with expansion underway.*
=======
# Windsurf Projects Template Generator

Production-ready Python project templates optimized for Windsurf IDE with state-of-the-art tooling and agentic AI integration.

## 🚀 Getting Started - Complete Process

### Prerequisites
- **Python 3.11+** 
- **Windsurf IDE**
- **Git** (for version control)

### Step 1: Setup Template Generator

```bash
# Navigate to the template generator
cd C:\Synaptix-Labs\projects\Windsurf-Projects-Template

# Install required dependencies
pip install copier pydantic rich typer

# Verify everything is ready
python scripts/check_dependencies.py
```

**Expected Output:** ✅ All dependencies and templates are ready!

### Step 2: Create Your New Project

```bash
# Create new project directory (use lowercase with hyphens)
mkdir C:\Synaptix-Labs\projects\<project-name>
cd C:\Synaptix-Labs\projects\<project-name>

# Example: For a 4-in-a-row game
mkdir C:\Synaptix-Labs\projects\my-4-in-a-row-game
cd C:\Synaptix-Labs\projects\my-4-in-a-row-game

# 💡 TIP: Directory name becomes default project name

# Generate project using template
python C:\Synaptix-Labs\projects\Windsurf-Projects-Template\scripts\windsurf_generate.py
```

**Interactive Process:**
- Choose template type (e.g., `python-game-development`)
- **Project name defaults to directory name** (press Enter to accept, or type new name)
- Provide project description and framework choice
- **Paste your project requirements** (if you have them)
- Configure testing level, documentation, CI/CD options

### Step 3: Open Project in Windsurf

```
1. In Windsurf: File → Open Folder
2. Navigate to: C:\Synaptix-Labs\projects\<project-name>
3. Verify generated structure:
   ✅ src/<project_name>/      # Main source code
   ✅ tests/                   # Test suite
   ✅ docs/                    # Documentation & TODOs
   ✅ .windsurfrules          # Windsurf configuration
   ✅ pyproject.toml          # Project configuration
```

### Step 4: Create Project-Specific TODOs

**You need to ask Windsurf to help create customized TODOs for your project:**
e.g. "I just generated this project. Can you help me create TODOs for my  game?"

**Or start implemeting based on existing TODOs**

#### 4a. Infrastructure TODOs (Already Created)
The `docs/` directory contains **prime infrastructure TODOs** for basic project setup:
- ✅ `docs/TODO.<project-name>.1.md` - Sprint 1 (Infrastructure setup)
- ✅ `docs/game_design.md` - Project requirements template

#### 4b. Project-Specific TODOs (User-Initiated)
**Ask Windsurf AI to help you create detailed implementation TODOs:**

```
👤 You: "I just generated this project. Can you help me create detailed TODOs 
        for my 4-in-a-row game with AI opponent?"

🤖 Windsurf: "I see you have infrastructure TODOs in docs/. Let me help you create 
             game-specific TODOs. Please provide your detailed game requirements, 
             or I can help you define them."

👤 You: [Provide requirements like: 'Connect 4 game, human vs AI, 3 difficulty 
        levels, pygame interface, minimax algorithm']

🤖 Windsurf: "Based on your requirements, I'll create additional TODO files:
             - docs/TODO.<project-name>.2.md (Core game logic)
             - docs/TODO.<project-name>.3.md (AI implementation) 
             - docs/TODO.<project-name>.4.md (Polish & testing)"
```

**Key Questions to Ask Windsurf:**
- "Help me create project-specific TODOs based on my requirements"
- "Analyze my game requirements and break them into sprint tasks"
- "Update the existing TODOs with my specific game features"
- "Create a development roadmap for my [game type] project"

### Step 5: Begin Development with Windsurf Guidance

**Windsurf AI leads the dynamic development process:**

#### 5a. Infrastructure First (Sprint 1)
```
🤖 Windsurf: "Let's start with Sprint 1 - Infrastructure setup. I'll guide you through:
             1. Python environment setup with Poetry
             2. Development tools configuration
             3. Testing infrastructure
             4. Basic project structure validation"

👤 User: "Start with Poetry setup"
🤖 Windsurf: [Executes: poetry install, poetry run pre-commit install, etc.]
```

#### 5b. Project-Specific Implementation (Sprint 2+)
```
🤖 Windsurf: "Infrastructure is ready! Now let's implement your game requirements.
             Based on your TODOs, shall we start with:
             - Game board data structure
             - Basic pygame window setup  
             - Core game logic
             - [Other options based on user requirements]"

👤 User: "Let's start with the game board"
🤖 Windsurf: [Helps implement based on requirements and TODOs]
```

## 🎯 Dynamic Process - User as Product Manager

**Important:** This is a **conversational, user-driven process**. Windsurf adapts to your needs:

### User Control Points
- **Change priorities:** "Skip the AI opponent for now, focus on basic gameplay"
- **Override suggestions:** "I want to use arcade instead of pygame"
- **Update requirements:** "Add multiplayer support to the TODOs"
- **Skip steps:** "I already have the environment set up"
- **Add features:** "Can we add sound effects to Sprint 3?"

### Windsurf Adapts Dynamically
- **Reorders tasks** based on user priorities
- **Updates TODOs** when requirements change
- **Suggests alternatives** when challenges arise
- **Tracks progress** and adjusts sprint planning
- **Provides context** from project documentation

### Example Dynamic Conversation
```
👤 User: "Actually, let's implement the AI opponent first, then worry about UI"

🤖 Windsurf: "Good idea! I'll reorder the TODOs. Since you want AI-first development:
             1. Let's implement the minimax algorithm core
             2. Create basic text-based testing for the AI
             3. Add pygame UI later
             
             Should I update docs/TODO.<project-name>.2.md to reflect this priority?"

👤 User: "Yes, and let's make the AI really challenging from the start"

🤖 Windsurf: "Perfect! I'll update the TODOs to include alpha-beta pruning in Sprint 2 
             instead of Sprint 3. Let's start with the game state representation..."
```

---

## 📁 Available Templates

### 🎮 **python-game-development**
- **Stack:** Python + pygame/arcade/pyglet + algorithmic AI
- **Use Cases:** 2D games, board games, AI opponents
- **Features:** Game loop, AI algorithms, testing infrastructure

### 🤖 **agentic-ai** 
- **Stack:** crew.ai + FastAPI + Pydantic v2 + Vector DBs
- **Use Cases:** Multi-agent systems, intelligent automation, RAG applications
- **Features:** Agent orchestration, tool integration, async processing

### 📊 **data-science**
- **Stack:** Polars + Prefect + Jupyter + DuckDB
- **Use Cases:** ETL pipelines, analytics, ML workflows
- **Features:** Fast data processing, workflow orchestration, notebooks

### 🌐 **web-api**
- **Stack:** FastAPI + SQLAlchemy + Pydantic v2
- **Use Cases:** REST APIs, microservices, backend services
- **Features:** Async endpoints, database integration, API documentation

### 🏗️ **agentic-medallion**
- **Stack:** crew.ai + Prefect + Multi-DB (Bronze→Silver→Gold)
- **Use Cases:** Data lakes, intelligent data processing, enterprise data platforms
- **Features:** Layered data architecture, AI-driven processing, multi-source integration

### 🔧 **custom-multi**
- **Stack:** Configurable combination of above
- **Use Cases:** Complex projects requiring multiple paradigms
- **Features:** Template composition, shared components, unified configuration

## 🛠️ Core Technology Stack

**Foundation:**
- **Python 3.11+** with modern async patterns
- **UV/Poetry** for dependency management
- **Ruff + MyPy** for code quality
- **Pytest + Hypothesis** for comprehensive testing

**Development Tools:**
- **Windsurf IDE** integration with project-specific `.windsurfrules`
- **Pre-commit hooks** for automated code quality
- **GitHub Actions** for CI/CD
- **Docker** for containerization
- **Sphinx/MkDocs** for documentation

## 🎯 Key Features

### Sprint-Based Development
- **Infrastructure-first approach** - Set up tooling before implementing features
- **User-driven TODO generation** - Based on your specific requirements
- **Dynamic sprint planning** - Windsurf adapts to your changing priorities
- **Progress tracking** - Clear milestones and definitions of done

### Windsurf Integration
- **Conversational development** - AI guides you through the process
- **Project-aware assistance** - AI understands your specific requirements
- **Automatic TODO management** - Integrated with Windsurf's TODO system
- **Context-aware suggestions** - Based on your project's `.windsurfrules`

### Production-Ready Output
- **Comprehensive testing** (unit, integration, performance)
- **Security-first** approach with pre-commit hooks and vulnerability scanning
- **Documentation automation** (API docs, user guides, architecture)
- **Deployment ready** (Docker, CI/CD, monitoring)

## 📚 Documentation Structure

Generated projects include:
- **`docs/TODO.<project-name>.*.md`** - Sprint-based development tasks
- **`docs/game_design.md`** - Project requirements and specifications
- **`docs/architecture.md`** - Technical architecture documentation
- **`.windsurfrules`** - Windsurf AI behavior configuration
- **`README.md`** - Project overview and setup instructions

## 🤝 Development Philosophy

**You are the Product Manager.** Windsurf is your intelligent development partner that:
- **Adapts to your vision** - Not the other way around
- **Suggests best practices** - But follows your decisions
- **Handles implementation details** - While you focus on requirements
- **Tracks progress** - And adjusts plans as needed
- **Provides context** - From your project documentation and history

## 🚀 Quick Start Commands

```bash
# Check if everything is ready
python scripts/check_dependencies.py

# Generate a new project (interactive)
cd your-new-project-directory
python C:\Synaptix-Labs\projects\Windsurf-Projects-Template\scripts\windsurf_generate.py

# Generate with defaults (non-interactive)
python C:\Synaptix-Labs\projects\Windsurf-Projects-Template\scripts\windsurf_generate.py --non-interactive

# Check available templates
python scripts/generate_project.py list-templates
```

## 🔧 Troubleshooting

**Common Issues:**
- **Copier not found:** `pip install copier`
- **Template not found:** Check `template-generators/` directory
- **Permission errors:** Run as administrator or check directory permissions
- **Windsurf can't find TODOs:** Ensure files are in `docs/` directory with correct naming

**Get Help:**
- Check `docs/windsurf-integration-guide.md` for detailed AI integration
- Review generated `.windsurfrules` for project-specific guidance
- Ask Windsurf AI: *"Help me understand my project structure"*

---

**🎮 Ready to build your next Python project with AI-powered development!** 

Start with Step 1 above, and let Windsurf guide you through the rest.

