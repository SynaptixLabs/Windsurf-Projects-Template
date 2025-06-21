#!/usr/bin/env python3
"""
Final validation script for enhanced template generator.
Verifies that all fixes work correctly and Sprint 0 template is comprehensive.
"""

import os
import shutil
import subprocess
from pathlib import Path

def test_template_generation():
    """Test the complete template generation process."""
    print("🧪 Testing Enhanced Template Generator...")
    
    # Setup paths
    template_dir = Path("C:/Synaptix-Labs/projects/Windsurf-Projects-Template/template-generators/python-game-development")
    test_output = Path("C:/Synaptix-Labs/projects/test-game-validation")
    
    # Clean up existing test
    if test_output.exists():
        print(f"Removing existing test directory: {test_output}")
        shutil.rmtree(test_output)
    
    # Test template generation
    print("\n1. Testing Copier template generation...")
    try:
        result = subprocess.run([
            "copier", "copy", 
            str(template_dir), 
            str(test_output),
            "--data", "project_name=test-game-validation",
            "--data", "project_description=Test game for validation",
            "--data", "author_name=Test Author",
            "--data", "author_email=test@example.com",
            "--data", "author_github_url=https://github.com/TestOrg",
            "--data", "python_version=3.12",
            "--data", "game_framework=pygame",
            "--data", "has_project_spec=false",
            "--data", "game_category=board_game",
            "--data", "testing_level=comprehensive",
            "--data", "documentation_level=standard",
            "--data", "include_cicd=true",
            "--data", "include_docker=false",
            "--data", "use_sprint_based_todos=true",
            "--data", "sprint_duration_weeks=2",
            "--data", "total_sprints=4",
            "--data", "include_performance_profiling=false",
            "--data", "include_logging=true",
            "--data", "include_config_management=true"
        ], capture_output=True, text=True, cwd="C:/Synaptix-Labs/projects")
        
        if result.returncode != 0:
            print(f"❌ Template generation failed: {result.stderr}")
            return False
        
        print("✅ Template generation successful")
        
    except Exception as e:
        print(f"❌ Error running Copier: {e}")
        return False
    
    # Verify generated structure
    print("\n2. Verifying generated project structure...")
    
    # Check Sprint TODO files
    todo_files = [
        "docs/TODO.test-game-validation.0.md",
        "docs/TODO.test-game-validation.1.md", 
        "docs/TODO.test-game-validation.2.md",
        "docs/TODO.test-game-validation.3.md"
    ]
    
    for todo_file in todo_files:
        todo_path = test_output / todo_file
        if todo_path.exists():
            print(f"✅ {todo_file} - EXISTS")
            # Check content
            content = todo_path.read_text(encoding='utf-8')
            if "Sprint" in content and "TODO" in content:
                print(f"   Content validated: Contains Sprint tasks")
            else:
                print(f"❌ {todo_file} - Invalid content")
                return False
        else:
            print(f"❌ {todo_file} - MISSING")
            return False
    
    # Check no unwanted directories
    template_backup = test_output / "template_backup_empty"
    if template_backup.exists():
        print("❌ template_backup_empty directory found (should be excluded)")
        return False
    else:
        print("✅ No template_backup_empty directory (correctly excluded)")
    
    # Check core infrastructure files
    infrastructure_files = [
        "src/test_game_validation/__init__.py",
        "src/test_game_validation/config/__init__.py",
        "src/test_game_validation/config/game_settings.py",
        "src/test_game_validation/core/__init__.py",
        "src/test_game_validation/core/constants.py",
        "src/test_game_validation/core/exceptions.py",
        "tests/conftest.py",
        "tests/unit/test_constants.py",
        "tests/unit/test_exceptions.py",
        "tests/unit/test_game_settings.py",
        ".windsurfrules",
        ".windsurf_config.yaml",
        ".github/workflows/ci.yml",
        ".pre-commit-config.yaml",
        "pyproject.toml",
        "pytest.ini",
        ".env.example"
    ]
    
    for file_path in infrastructure_files:
        full_path = test_output / file_path
        if full_path.exists():
            print(f"✅ {file_path} - EXISTS")
        else:
            print(f"❌ {file_path} - MISSING")
            return False
    
    # Test Python imports
    print("\n3. Testing Python module imports...")
    os.chdir(test_output)
    
    try:
        # Test settings import
        result = subprocess.run([
            "python", "-c", 
            "import sys; sys.path.insert(0, 'src'); from test_game_validation.config import settings; print(f'Settings: {settings.game_title}')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Settings import successful")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ Settings import failed: {result.stderr}")
            return False
        
        # Test constants import
        result = subprocess.run([
            "python", "-c",
            "import sys; sys.path.insert(0, 'src'); from test_game_validation.core.constants import Colors, GameState; print(f'Constants: {Colors.PLAYER_1}, {GameState.PLAYING}')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Constants import successful")
            print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"❌ Constants import failed: {result.stderr}")
            return False
        
        # Test exceptions import
        result = subprocess.run([
            "python", "-c",
            "import sys; sys.path.insert(0, 'src'); from test_game_validation.core.exceptions import GameError, InvalidMoveError; print('Exceptions imported successfully')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Exceptions import successful")
        else:
            print(f"❌ Exceptions import failed: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"❌ Error testing imports: {e}")
        return False
    
    print("\n🎉 All validation tests passed!")
    print("\nGenerated project structure:")
    
    # Show directory tree
    for root, dirs, files in os.walk(test_output):
        level = root.replace(str(test_output), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files[:5]:  # Limit to first 5 files per directory
            print(f"{subindent}{file}")
        if len(files) > 5:
            print(f"{subindent}... and {len(files) - 5} more files")
    
    return True

def main():
    """Run validation tests."""
    print("Enhanced Template Generator Validation")
    print("=" * 50)
    
    success = test_template_generation()
    
    if success:
        print("\n✅ VALIDATION PASSED")
        print("Enhanced template generator is working correctly!")
        print("\nKey improvements verified:")
        print("• 4 Sprint TODO files generated (0-3)")
        print("• template_backup_empty directory excluded")
        print("• Complete infrastructure files created")
        print("• Python modules import successfully")
        print("• Game settings, constants, and exceptions working")
    else:
        print("\n❌ VALIDATION FAILED")
        print("Issues found in template generator. Review errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
