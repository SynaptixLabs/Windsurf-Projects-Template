# Prime Script: Game Development Project

## 🎮 Windsurf Execution Commands for Game Development

### Phase 1: Project Infrastructure Setup

**Execute the following commands in sequence:**

1. **Initialize Project Structure**
   ```bash
   # Verify Python 3.11+ is available
   python --version
   
   # Initialize Poetry project
   poetry init --no-interaction
   poetry config virtualenvs.in-project true
   poetry install
   ```

2. **Setup Development Environment**
   ```bash
   # Install development dependencies
   poetry add --group dev pytest pytest-asyncio pytest-mock pytest-cov
   poetry add --group dev ruff mypy black pre-commit
   poetry add --group dev sphinx sphinx-autoapi furo
   
   # Install game development dependencies
   poetry add pygame pydantic typer rich
   poetry add --group dev hypothesis pytest-benchmark
   
   # Setup pre-commit hooks
   poetry run pre-commit install
   ```

3. **Create Project Structure**
   ```bash
   # Create source directories
   mkdir -p src/{{project_name}}
   mkdir -p src/{{project_name}}/core
   mkdir -p src/{{project_name}}/ai
   mkdir -p src/{{project_name}}/ui
   mkdir -p src/{{project_name}}/utils
   
   # Create test directories
   mkdir -p tests/unit
   mkdir -p tests/integration
   mkdir -p tests/performance
   
   # Create documentation directories
   mkdir -p docs/source
   mkdir -p docs/game_design
   ```

4. **Generate Initial TODO List**
   ```bash
   # Generate Sprint 1 TODO list
   python scripts/todo_generator.py --project "{{project_name}}" --template game-development --sprint 1
   ```

### Phase 2: Core Game Engine Development

**Sprint 1 Focus: Basic Game Foundation**

1. **Create Core Game Classes**
   - Implement `GameBoard` class for game state management
   - Create `GameEngine` class for game loop and logic
   - Add `Player` and `AIPlayer` base classes

2. **Setup Pygame Foundation**
   - Initialize pygame window and display
   - Implement basic event handling (mouse, keyboard)
   - Create rendering system for game board

3. **Basic Game Logic**
   - Implement move validation
   - Add win condition detection (4-in-a-row)
   - Create turn management system

**Commands to execute:**
```bash
# Run tests after each major component
poetry run pytest tests/unit/ -v

# Check code quality
poetry run ruff check src/
poetry run mypy src/

# Run game to test basic functionality
poetry run python src/{{project_name}}/main.py
```

### Phase 3: AI Implementation

**Sprint 2-3 Focus: AI Opponent Development**

1. **Novice AI (Random + Basic Heuristics)**
   - Random move selection from valid moves
   - Basic column preference (favor center)
   - Simple threat detection

2. **Intermediate AI (Minimax Algorithm)**
   - Implement minimax with limited depth (3-4 levels)
   - Add position evaluation function
   - Basic optimization for performance

3. **Expert AI (Advanced Minimax)**
   - Alpha-beta pruning optimization
   - Increased search depth (6-8 levels)  
   - Opening book for first moves
   - Advanced position evaluation

**Commands to execute:**
```bash
# Test AI algorithms specifically
poetry run pytest tests/unit/test_ai.py -v

# Benchmark AI performance
poetry run pytest tests/performance/ --benchmark-only

# Profile AI decision making
poetry run python -m cProfile -o ai_profile.prof src/{{project_name}}/ai/minimax.py
```

### Phase 4: Testing & Quality Assurance

**Sprint 4 Focus: Comprehensive Testing**

1. **Unit Testing**
   - Test all game logic components
   - Test AI algorithms with known positions
   - Mock pygame components for headless testing

2. **Integration Testing**
   - Test complete game workflows
   - Test human vs AI gameplay
   - Test AI vs AI gameplay for balance

3. **Performance Testing**
   - Benchmark AI response times
   - Test memory usage during long games
   - Profile rendering performance

**Commands to execute:**
```bash
# Run complete test suite
poetry run pytest --cov=src/{{project_name}} --cov-report=html

# Run performance benchmarks
poetry run pytest tests/performance/ --benchmark-save=game_benchmarks

# Generate test report
poetry run pytest --html=reports/test_report.html
```

### Phase 5: Documentation & Finalization

**Sprint 4 Focus: Documentation & Polish**

1. **Code Documentation**
   ```bash
   # Generate API documentation
   poetry run sphinx-build docs/source docs/_build/html
   
   # Update README with gameplay instructions
   # Add architecture documentation
   # Create development setup guide
   ```

2. **Game Polish**
   - Add visual effects and animations
   - Implement sound effects (optional)
   - Create difficulty selection menu
   - Add game statistics tracking

3. **Deployment Preparation**
   ```bash
   # Build standalone executable (optional)
   poetry add --group dev pyinstaller
   poetry run pyinstaller --onefile src/{{project_name}}/main.py
   
   # Create distribution package
   poetry build
   ```

## 🎯 Sprint Completion Checklist

### Sprint 1 ✅
- [ ] Project structure created and configured
- [ ] Poetry environment setup and dependencies installed
- [ ] Basic pygame window and event handling working
- [ ] Core game board and logic implemented
- [ ] Unit tests for core functionality passing
- [ ] Pre-commit hooks configured and passing

### Sprint 2 ✅
- [ ] Novice AI implemented and functional
- [ ] Intermediate AI with minimax algorithm working
- [ ] AI vs Human gameplay fully functional
- [ ] Performance benchmarks established
- [ ] Integration tests for gameplay scenarios passing

### Sprint 3 ✅
- [ ] Expert AI with alpha-beta pruning implemented
- [ ] Difficulty selection menu functional
- [ ] Game restart and statistics features working
- [ ] Performance optimizations completed
- [ ] All AI levels properly balanced

### Sprint 4 ✅
- [ ] Comprehensive test suite with >90% coverage
- [ ] Complete documentation generated
- [ ] Code quality metrics passing (Ruff, MyPy)
- [ ] Performance benchmarks within acceptable ranges
- [ ] Game ready for distribution

## 🚀 Windsurf Integration Notes

**Windsurf-Specific Commands:**
- Use `poetry run python -m {{project_name}}` for consistent module execution
- Leverage Windsurf's TODO integration for sprint tracking
- Use Windsurf's code generation for boilerplate AI algorithms
- Utilize Windsurf's refactoring tools for code optimization

**Git Workflow:**
```bash
# After each sprint completion
git add .
git commit -m "Complete Sprint X: [brief description]"
git push origin main

# Tag major milestones
git tag -a v0.1.0 -m "Basic gameplay functional"
git tag -a v0.2.0 -m "AI opponent implemented"
git tag -a v0.3.0 -m "All difficulty levels complete"
git tag -a v1.0.0 -m "Production ready release"
git push origin --tags
```

**Continuous Integration:**
- Tests run automatically on commit (pre-commit hooks)
- GitHub Actions validate code quality and run test suite
- Automated documentation builds on successful tests
- Performance regression detection in CI pipeline

---

**Template Generation Date:** {{generation_date}}
**Project Type:** Game Development
**AI Complexity:** Novice → Intermediate → Expert
**Estimated Total Development Time:** 60-80 hours across 4 sprints
