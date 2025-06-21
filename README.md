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
