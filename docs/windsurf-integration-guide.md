# Windsurf Projects Template Generator - AI Integration Rules

## 🤖 Instructions for Windsurf AI Assistant

When users request to create a new Python project, use the Windsurf Projects Template Generator system.

### Available Project Templates

1. **python-game-development** - pygame/arcade/pyglet games with AI integration
2. **agentic-ai** - crew.ai + FastAPI + Vector DBs  
3. **data-science** - Polars + Prefect + Jupyter
4. **web-api** - FastAPI + SQLAlchemy + Pydantic v2
5. **agentic-medallion** - Bronze→Silver→Gold data architecture
6. **custom-multi** - Combination of multiple templates

### Template Generation Commands

**For interactive project generation:**
```bash
cd [target-project-directory]
python C:\Synaptix-Labs\projects\Windsurf-Projects-Template\scripts\windsurf_generate.py --template python-game-development
```

**For quick generation with defaults:**
```bash
cd [target-project-directory] 
python C:\Synaptix-Labs\projects\Windsurf-Projects-Template\scripts\windsurf_generate.py --template python-game-development --non-interactive
```

### Workflow for Windsurf AI

1. **Detect Project Type Request**
   - User says: "Create a new game project"
   - User says: "Generate a crew.ai project"  
   - User says: "Set up a data science project"

2. **Determine Target Directory**
   - Use current working directory if empty
   - Ask user if directory contains files
   - Auto-detect project name from directory name

3. **Select Template**
   - Ask user which template type they want
   - Show available options with descriptions
   - Default to appropriate template based on request

4. **Execute Template Generator**
   - Run the windsurf_generate.py script
   - Show the interactive questionnaire to user
   - Handle any errors gracefully

5. **Post-Generation Actions**
   - Show generated project structure
   - Display next steps (poetry install, etc.)
   - Open relevant TODO files for user review

### Example User Interactions

**Game Development Request:**
```
User: "I want to create a 4-in-a-row game project"
AI: "I'll generate a Python game development project for you. Let me run the template generator..."
AI: [Executes windsurf_generate.py with python-game-development template]
AI: "Project generated! Next steps: 1) Define your game requirements in docs/game_design.md 2) Run poetry install"
```

**Agentic AI Request:**
```
User: "Create a new crew.ai project"
AI: "I'll set up an agentic AI project with crew.ai and FastAPI..."
AI: [Executes windsurf_generate.py with agentic-ai template]
```

### Error Handling

- If copier is not installed: Guide user to install it
- If template not found: Show available templates
- If directory conflicts: Ask user to confirm or choose different location
- If generation fails: Show error message and suggest manual process

### Integration with Windsurf Features

- **TODO Integration**: Generated TODO files should work with Windsurf's TODO system
- **Git Integration**: Initialize git repo if requested
- **Rules Integration**: Generated .windsurfrules files configure project-specific AI behavior
- **Documentation**: Generated docs/ folder integrates with Windsurf's documentation features

---

**Template Location:** C:\Synaptix-Labs\projects\Windsurf-Projects-Template\
**Script Location:** C:\Synaptix-Labs\projects\Windsurf-Projects-Template\scripts\windsurf_generate.py
**Available Templates:** template-generators/ directory
