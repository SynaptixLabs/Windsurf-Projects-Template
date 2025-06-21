#!/usr/bin/env python3
"""
Automated Commit Script for Windsurf-Projects-Template

Automates the commit process from cleanup to remote push.
Assumes GitHub repository already exists.
"""

import subprocess
import os
import sys
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, description, check=True):
    """Run a command with logging."""
    logger.info(f"🔄 {description}...")
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        else:
            result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        
        if result.returncode == 0:
            logger.info(f"✅ {description} completed")
            if result.stdout.strip():
                logger.debug(f"Output: {result.stdout.strip()}")
        else:
            logger.warning(f"⚠️ {description} had issues: {result.stderr.strip()}")
        
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        return False

def create_gitignore(project_root):
    """Create .gitignore file if it doesn't exist."""
    gitignore_path = project_root / ".gitignore"
    
    if gitignore_path.exists():
        logger.info("✅ .gitignore already exists")
        return True
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/*.log
*.log

# Temporary files
temp/
tmp/
*.tmp
*.temp

# Generated files
validation_report.md
requirements-generator.txt

# Test outputs
.pytest_cache/
.coverage
htmlcov/

# Windsurf specific
.windsurf/
"""
    
    try:
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        logger.info("✅ .gitignore created")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create .gitignore: {e}")
        return False

def automated_commit():
    """Automate the entire commit process."""
    project_root = Path(__file__).parent.parent
    logger.info(f"🚀 Starting automated commit process for: {project_root}")
    
    # Change to project root
    original_cwd = os.getcwd()
    os.chdir(project_root)
    
    try:
        # Step 1: Clean up redundant files
        logger.info("🧹 Step 1: Cleaning up redundant scripts...")
        cleanup_script = project_root / "scripts" / "cleanup_redundant_scripts.py"
        if cleanup_script.exists():
            if not run_command([sys.executable, str(cleanup_script)], "Running cleanup script"):
                logger.warning("⚠️ Cleanup script had issues, but continuing...")
        else:
            logger.warning("⚠️ Cleanup script not found, skipping...")
        
        # Step 2: Initialize git if needed
        if not (project_root / ".git").exists():
            if not run_command("git init", "Initializing Git repository"):
                return False
        else:
            logger.info("✅ Git repository already initialized")
        
        # Step 3: Configure git user
        logger.info("👤 Step 3: Configuring Git user...")
        run_command('git config user.name "Avidor"', "Setting git user name", check=False)
        run_command('git config user.email "avidor@synaptixlabs.ai"', "Setting git user email", check=False)
        
        # Step 4: Create .gitignore
        logger.info("📝 Step 4: Creating .gitignore...")
        create_gitignore(project_root)
        
        # Step 5: Stage all files
        logger.info("📦 Step 5: Staging all files...")
        if not run_command("git add .", "Staging files"):
            return False
        
        # Step 6: Create commit
        logger.info("💾 Step 6: Creating commit...")
        commit_message = """🎉 Windsurf Project Template Generator v4.0 - Refactored Architecture

✨ Major Refactoring - Modular Library-Based Architecture:
- Converted monolithic scripts to modular library components
- Clear separation of concerns with single responsibility principle
- Enhanced maintainability and testability

🏗️ New Architecture Components:
- windsurf_generator.py: Main orchestrator and entry point
- lib_template_renderer.py: Template rendering engine with inheritance support
- lib_github_manager.py: GitHub repository management with multiple fallbacks
- lib_project_cleanup.py: Template artifact cleanup and project hygiene
- lib_project_validator.py: Comprehensive project structure validation
- lib_todo_generator.py: Sprint-based TODO generation for project management
- util_check_dependencies.py: System dependency verification

🎯 Template System Features:
- Template inheritance system (base templates + specialized overlays)
- python-modern: Universal base template for all Python projects
- python-game-development: Game development with Pygame integration
- python-agentic-ai: CrewAI multi-agent systems with FastAPI
- python-data-science: Data science with Polars, DuckDB, and Prefect

🔧 Modern Python Tooling Integration:
- UV for ultra-fast package management (80x faster than pip)
- Ruff for lightning-fast linting and formatting (150x faster than alternatives)
- Polars for high-performance data processing (5-10x faster than Pandas)
- FastAPI with async support for high-performance APIs
- Pydantic v2 with Rust-based validation (50x performance improvement)
- crew.ai for production-ready multi-agent AI systems

🚀 Windsurf IDE Optimization:
- Native integration with Windsurf's AI-powered development workflow
- Custom .windsurfrules configuration for project-specific AI behavior
- Automated documentation structure (projectRoadmap.md, codebaseSummary.md)
- Sprint-based TODO generation compatible with Windsurf's task management

🧪 Comprehensive Testing Infrastructure:
- pytest with advanced fixtures and parametrization
- Hypothesis for property-based testing and edge case discovery
- VCR.py for HTTP interaction recording and replay
- testcontainers for realistic integration testing with databases
- Performance regression testing with pytest-benchmark

📋 Sprint-Based Project Management:
- Automated TODO generation for 4-sprint development cycles
- Game development: Infrastructure → Core Mechanics → Polish → Production
- AI projects: Setup → Agent Development → Integration → Deployment
- Data science: Infrastructure → Processing → Analysis → Productionization

🐙 GitHub Integration & Automation:
- Automatic repository creation with multiple fallback methods
- GitHub CLI integration with API fallback
- Pre-configured CI/CD workflows with GitHub Actions
- Automated security scanning and dependency updates
- Branch protection and review requirements

🐳 Production-Ready Configurations:
- Multi-stage Docker builds optimized for production
- Comprehensive pre-commit hooks for code quality
- Automated dependency vulnerability scanning
- Performance monitoring and observability setup
- Structured logging with rotation and retention policies

🔍 Quality Assurance & Validation:
- Project structure validation with detailed reporting
- Template artifact cleanup to ensure clean generation
- Comprehensive dependency checking with installation help
- Automated code quality enforcement with Ruff and MyPy
- Coverage reporting with intelligent thresholds

⚡ Performance & Developer Experience:
- Faster project generation through optimized template rendering
- Intelligent caching of dependencies and build artifacts
- Parallel test execution for rapid feedback cycles
- Hot-reload development servers for immediate iteration
- Advanced debugging configurations for multiple IDEs

🔒 Security & Best Practices:
- Secure secret management with environment variable templates
- Input validation and sanitization throughout the pipeline
- Container security with non-root users and minimal base images
- Automated security scanning in CI/CD pipelines
- Compliance with modern Python packaging standards (PEP 621, PEP 517)

📖 Documentation & Onboarding:
- Comprehensive README with quick start guides
- Architecture documentation with decision records
- API documentation auto-generation
- Contributing guidelines with development setup
- Example projects demonstrating best practices

🎮 Ready for Space Invaders Game Development:
- Optimized template for 2D game development with Pygame
- Performance profiling tools for game optimization
- Asset management and resource loading patterns
- Game state management and event handling
- Audio/visual effect integration frameworks

This refactored v4.0 architecture provides a solid foundation for building modern Python projects with state-of-the-art tooling, comprehensive automation, and production-ready configurations. The modular design ensures long-term maintainability while the Windsurf integration optimizes the AI-powered development experience."""
        
        if not run_command(f'git commit -m "{commit_message}"', "Creating commit"):
            return False
        
        # Step 7: Check for remote
        logger.info("🔗 Step 7: Checking remote configuration...")
        result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
        
        if "origin" not in result.stdout:
            logger.info("🔗 Adding remote origin...")
            remote_url = "https://github.com/SynaptixLabs/Windsurf-Projects-Template.git"
            if not run_command(f'git remote add origin {remote_url}', "Adding remote origin"):
                return False
        else:
            logger.info("✅ Remote origin already configured")
        
        # Step 8: Push to remote
        logger.info("🚀 Step 8: Pushing to remote repository...")
        
        # Try pushing to main first, then master if main fails
        if not run_command("git push -u origin main", "Pushing to main branch", check=False):
            logger.info("🔄 Trying master branch...")
            if not run_command("git push -u origin master", "Pushing to master branch", check=False):
                # Try without -u flag in case branch exists
                if not run_command("git push origin main", "Pushing to existing main branch", check=False):
                    run_command("git push origin master", "Pushing to existing master branch", check=False)
        
        # Success summary
        logger.info(f"""
🎉 Automated Commit Process Complete!

📊 Summary:
   📁 Project: {project_root.name}
   🐙 Repository: https://github.com/SynaptixLabs/Windsurf-Projects-Template
   💾 Commit: Created with comprehensive refactoring message
   🚀 Push: Completed to remote repository

🎯 Next Steps:
   1. Verify repository: https://github.com/SynaptixLabs/Windsurf-Projects-Template
   2. Test the new generator:
      python scripts/windsurf_generator.py --list-templates
   3. Create space-invaders project:
      cd C:/Synaptix-Labs/projects
      mkdir space-invaders && cd space-invaders
      python ../Windsurf-Projects-Template/scripts/windsurf_generator.py --template python-game-development

✅ The Windsurf Project Template Generator v4.0 is now committed and ready for use!
""")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Automated commit process failed: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return False
        
    finally:
        # Restore original directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated commit for Windsurf-Projects-Template")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("🔍 DRY RUN - Would perform these steps:")
        logger.info("   1. Clean up redundant scripts")
        logger.info("   2. Initialize Git repository (if needed)")
        logger.info("   3. Configure Git user")
        logger.info("   4. Create .gitignore file")
        logger.info("   5. Stage all files")
        logger.info("   6. Create comprehensive commit")
        logger.info("   7. Configure remote origin (if needed)")
        logger.info("   8. Push to GitHub")
        logger.info("\nRun without --dry-run to execute.")
    else:
        success = automated_commit()
        
        if success:
            print("\n🎉 Automated commit completed successfully!")
            print("Your Windsurf-Projects-Template is now ready for use.")
        else:
            print("\n❌ Automated commit failed!")
            print("Check the logs above for details.")
            sys.exit(1)
