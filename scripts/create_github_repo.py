#!/usr/bin/env python3
"""
GitHub Repository Setup for Windsurf-Projects-Template

This script creates the GitHub repository for the Windsurf project template system
and prepares it for initial commit with the refactored v4.0 architecture.
"""

import subprocess
import os
import sys
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def create_windsurf_template_repo():
    """Create GitHub repository for Windsurf-Projects-Template."""
    
    project_root = Path(__file__).parent.parent  # Go up from scripts/ to project root
    project_name = "Windsurf-Projects-Template"
    description = "Production-ready Python project template generator optimized for Windsurf IDE with modern tooling, agentic AI support, and comprehensive automation"
    org = "SynaptixLabs"
    
    logger.info(f"🚀 Setting up GitHub repository: {org}/{project_name}")
    logger.info(f"📁 Project root: {project_root}")
    
    # Change to project root directory
    original_cwd = os.getcwd()
    os.chdir(project_root)
    
    try:
        # Step 1: Check if GitHub CLI is available
        logger.info("🔍 Checking GitHub CLI availability...")
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            logger.error("❌ GitHub CLI not available")
            logger.error("Install GitHub CLI: https://cli.github.com/")
            return False
        
        logger.info(f"✅ GitHub CLI available: {result.stdout.strip()}")
        
        # Step 2: Check authentication
        logger.info("🔐 Checking GitHub authentication...")
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, check=False)
        
        if result.returncode != 0:
            logger.error("❌ GitHub CLI not authenticated")
            logger.error("Run: gh auth login")
            return False
        
        logger.info("✅ GitHub CLI authenticated")
        
        # Step 3: Initialize git repository if not already done
        logger.info("📦 Initializing Git repository...")
        if not (project_root / ".git").exists():
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            logger.info("✅ Git repository initialized")
        else:
            logger.info("✅ Git repository already exists")
        
        # Step 4: Configure git user
        logger.info("👤 Configuring Git user...")
        try:
            subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run(['git', 'config', 'user.name', 'Avidor'], check=True, capture_output=True)
            
        try:
            subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run(['git', 'config', 'user.email', 'avidor@synaptixlabs.ai'], check=True, capture_output=True)
        
        logger.info("✅ Git user configured")
        
        # Step 5: Create .gitignore if it doesn't exist
        gitignore_path = project_root / ".gitignore"
        if not gitignore_path.exists():
            logger.info("📝 Creating .gitignore...")
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
            gitignore_path.write_text(gitignore_content, encoding='utf-8')
            logger.info("✅ .gitignore created")
        
        # Step 6: Create README.md if it doesn't exist
        readme_path = project_root / "README.md"
        if not readme_path.exists():
            logger.info("📝 Creating README.md...")
            readme_content = f"""# {project_name}

Production-ready Python project template generator optimized for Windsurf IDE with modern 2025 tooling, agentic AI support, and comprehensive automation.

## 🚀 Features

- **Windsurf IDE Integration**: Native support for Windsurf's AI-powered development workflow
- **Modern Python Stack**: UV, Ruff, Polars, FastAPI, Pydantic v2, crew.ai
- **Template Inheritance**: Modular template system with base templates and specialized overlays
- **Agentic AI Support**: Built-in crew.ai integration for multi-agent systems
- **Comprehensive Testing**: pytest, Hypothesis, VCR.py, testcontainers
- **Sprint-Based Workflow**: Automated TODO generation with sprint planning
- **GitHub Integration**: Automatic repository creation and CI/CD setup
- **Production Ready**: Docker, pre-commit hooks, comprehensive documentation

## 📋 Available Templates

- **python-modern**: Base template for all Python projects
- **python-game-development**: Game development with Pygame
- **python-agentic-ai**: CrewAI multi-agent systems
- **python-data-science**: Data science with Polars and Prefect

## 🎯 Quick Start

```bash
# Navigate to your project directory
cd /path/to/your/new/project

# Run the generator (interactive mode)
python /path/to/Windsurf-Projects-Template/scripts/windsurf_generator.py

# Or specify template directly
python /path/to/Windsurf-Projects-Template/scripts/windsurf_generator.py --template python-game-development
```

## 🏗️ Architecture v4.0

Refactored modular architecture with clear separation of concerns:

- `windsurf_generator.py` - Main orchestrator
- `lib_template_renderer.py` - Template rendering engine
- `lib_github_manager.py` - GitHub repository management
- `lib_project_cleanup.py` - Artifact cleanup
- `lib_project_validator.py` - Project validation
- `lib_todo_generator.py` - Sprint-based TODO generation
- `util_check_dependencies.py` - Dependency verification

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE_v4.md)
- [Template Development](docs/template-development.md)
- [Usage Guide](docs/usage-guide.md)
- [Contributing](docs/contributing.md)

## 🔧 Requirements

- Python 3.9+
- Git
- GitHub CLI (optional, for automatic repo creation)

Required packages:
```bash
pip install copier pydantic requests
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and validation
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

Built for the modern Python development ecosystem with inspiration from:
- Windsurf IDE's AI-native development approach
- FastAPI's performance and developer experience
- crew.ai's multi-agent collaboration patterns
- Modern Python tooling (Ruff, UV, Polars)

---

**Version:** 4.0 (Refactored Architecture)  
**Author:** Avidor Rabinovich  
**Organization:** SynaptixLabs  
"""
            readme_path.write_text(readme_content, encoding='utf-8')
            logger.info("✅ README.md created")
        
        # Step 7: Stage all files
        logger.info("📦 Staging files for commit...")
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
        
        # Step 8: Create initial commit
        logger.info("💾 Creating initial commit...")
        commit_message = """🎉 Initial commit: Windsurf Project Template Generator v4.0

✨ Features:
- Modular library-based architecture (refactored from monolithic scripts)
- Template inheritance system with base templates and overlays
- Windsurf IDE integration with AI-powered development workflow
- Modern Python tooling (UV, Ruff, Polars, FastAPI, Pydantic v2)
- Agentic AI support with crew.ai integration
- Comprehensive testing infrastructure (pytest, Hypothesis, VCR.py)
- Sprint-based TODO generation and project management
- GitHub repository automation with multiple fallback methods
- Production-ready configurations (Docker, CI/CD, pre-commit hooks)

🏗️ Architecture:
- windsurf_generator.py: Main orchestrator
- lib_template_renderer.py: Template rendering engine  
- lib_github_manager.py: GitHub repository management
- lib_project_cleanup.py: Artifact cleanup
- lib_project_validator.py: Project validation
- lib_todo_generator.py: Sprint-based TODO generation
- util_check_dependencies.py: Dependency verification

📋 Templates:
- python-modern: Base template for all Python projects
- python-game-development: Game development with Pygame
- python-agentic-ai: CrewAI multi-agent systems
- python-data-science: Data science with Polars and Prefect

🎯 Ready for production use with comprehensive automation and modern tooling.
"""
        
        result = subprocess.run(['git', 'commit', '-m', commit_message], 
                               capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            logger.info("✅ Initial commit created")
        else:
            logger.warning(f"⚠️ Commit may have issues: {result.stderr}")
        
        # Step 9: Create GitHub repository
        logger.info(f"🐙 Creating GitHub repository: {org}/{project_name}")
        
        cmd = [
            'gh', 'repo', 'create', f"{org}/{project_name}",
            '--public',
            '--description', description,
            '--add-readme=false'  # We already have README
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            repo_url = f"https://github.com/{org}/{project_name}"
            logger.info(f"✅ GitHub repository created: {repo_url}")
        else:
            error_msg = result.stderr.strip()
            if "already exists" in error_msg.lower():
                repo_url = f"https://github.com/{org}/{project_name}"
                logger.info(f"ℹ️ Repository already exists: {repo_url}")
            else:
                logger.error(f"❌ GitHub repository creation failed: {error_msg}")
                return False
        
        # Step 10: Set up remote origin
        logger.info("🔗 Setting up remote origin...")
        remote_url = f"git@github.com:{org}/{project_name}.git"
        
        # Remove existing origin if it exists
        subprocess.run(['git', 'remote', 'remove', 'origin'], capture_output=True, check=False)
        
        # Add new origin
        subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True, capture_output=True)
        logger.info(f"✅ Remote origin set: {remote_url}")
        
        # Step 11: Push to GitHub
        logger.info("🚀 Pushing to GitHub...")
        result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                               capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            logger.info("✅ Successfully pushed to GitHub")
        else:
            # Try master branch
            result = subprocess.run(['git', 'push', '-u', 'origin', 'master'], 
                                   capture_output=True, text=True, check=False)
            if result.returncode == 0:
                logger.info("✅ Successfully pushed to GitHub (master branch)")
            else:
                logger.warning(f"⚠️ Push may have issues: {result.stderr}")
        
        # Success summary
        logger.info(f"""
🎉 GitHub Repository Setup Complete!

📊 Repository Details:
   🐙 URL: {repo_url}
   📁 Local: {project_root}
   🔗 Remote: {remote_url}

🎯 Next Steps:
   1. Run cleanup script to remove redundant files:
      python scripts/cleanup_redundant_scripts.py
   
   2. Test the new generator:
      python scripts/windsurf_generator.py --list-templates
   
   3. Create a test project:
      mkdir test-project && cd test-project
      python ../Windsurf-Projects-Template/scripts/windsurf_generator.py
   
   4. Update documentation and add examples
   
   5. Set up CI/CD workflows for template validation

🚀 The Windsurf Project Template Generator v4.0 is ready for use!
""")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Repository setup failed: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return False
        
    finally:
        # Restore original directory
        os.chdir(original_cwd)

def create_license_file():
    """Create MIT license file."""
    project_root = Path(__file__).parent.parent
    license_path = project_root / "LICENSE"
    
    if license_path.exists():
        logger.info("✅ LICENSE file already exists")
        return
    
    license_content = """MIT License

Copyright (c) 2025 Avidor Rabinovich / SynaptixLabs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    license_path.write_text(license_content, encoding='utf-8')
    logger.info("✅ LICENSE file created")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup GitHub repository for Windsurf-Projects-Template")
    parser.add_argument("--license-only", action="store_true", help="Only create LICENSE file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("🔍 DRY RUN - Would perform the following actions:")
        logger.info("   1. Check GitHub CLI availability and authentication")
        logger.info("   2. Initialize Git repository if needed")
        logger.info("   3. Configure Git user")
        logger.info("   4. Create .gitignore and README.md if needed")
        logger.info("   5. Create LICENSE file")
        logger.info("   6. Stage all files and create initial commit")
        logger.info("   7. Create GitHub repository: SynaptixLabs/Windsurf-Projects-Template")
        logger.info("   8. Set up remote origin and push to GitHub")
        logger.info("\nRun without --dry-run to execute these actions.")
    elif args.license_only:
        create_license_file()
    else:
        create_license_file()
        success = create_windsurf_template_repo()
        
        if success:
            print("\n🎉 Repository setup completed successfully!")
            print("The Windsurf-Projects-Template system is now ready for use.")
        else:
            print("\n❌ Repository setup failed!")
            print("Check the logs above for error details.")
            sys.exit(1)
