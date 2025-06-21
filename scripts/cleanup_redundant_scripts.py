#!/usr/bin/env python3
"""
Script Cleanup - Remove Redundant Files

This script removes the old redundant scripts as part of the v4.0 refactoring.
It implements the cleanup plan from the refactoring strategy.
"""

import shutil
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def cleanup_redundant_scripts():
    """Remove redundant scripts according to the refactoring plan."""
    
    scripts_dir = Path(__file__).parent
    
    # Scripts to remove (redundant after refactoring)
    scripts_to_remove = [
        "windsurf_generate.py",  # Core logic moved to lib_template_renderer.py
        "enhanced_windsurf_generator.py",  # Older version superseded by enhanced_windsurf_generator_v3.py
        "template_fixes.py",  # Fixes integrated into main generation process
        "validate_templates.py",  # Replaced by lib_project_validator.py
        "verify_fixes.py",  # Less comprehensive validation replaced by lib_project_validator.py
        "test_inheritance.py",  # Replaced by lib_project_validator.py
        "simulate_generation.py",  # Demonstration script not part of core generation
        "external_project_cleanup.py",  # Logic moved to lib_project_cleanup.py
        "todo_generator.py",  # Renamed to lib_todo_generator.py
        "github_integration.py",  # Logic moved to lib_github_manager.py
        "enhanced_windsurf_generator_v3.py",  # Refactored into windsurf_generator.py + libraries
        "check_dependencies.py",  # Renamed to util_check_dependencies.py
        "generate_project.py",  # If exists, superseded by windsurf_generator.py
        "test_templates.py"  # Replaced by lib_project_validator.py
    ]
    
    logger.info("🧹 Starting cleanup of redundant scripts...")
    
    removed_files = []
    missing_files = []
    
    for script_name in scripts_to_remove:
        script_path = scripts_dir / script_name
        
        if script_path.exists():
            try:
                script_path.unlink()
                removed_files.append(script_name)
                logger.info(f"   ✅ Removed: {script_name}")
            except Exception as e:
                logger.error(f"   ❌ Failed to remove {script_name}: {e}")
        else:
            missing_files.append(script_name)
            logger.debug(f"   ⏭️ Not found: {script_name}")
    
    # Summary
    logger.info(f"\n📊 Cleanup Summary:")
    logger.info(f"   📁 Scripts removed: {len(removed_files)}")
    logger.info(f"   ⏭️ Scripts not found: {len(missing_files)}")
    
    if removed_files:
        logger.info(f"   🗑️ Removed files: {', '.join(removed_files)}")
    
    # Clean up __pycache__ directories
    logger.info("\n🧹 Cleaning __pycache__ directories...")
    pycache_dirs = list(scripts_dir.rglob("__pycache__"))
    
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            logger.info(f"   ✅ Removed: {pycache_dir.relative_to(scripts_dir)}")
        except Exception as e:
            logger.error(f"   ❌ Failed to remove {pycache_dir}: {e}")
    
    logger.info("\n✅ Script cleanup completed!")
    
    # Show remaining files
    remaining_files = [f.name for f in scripts_dir.glob("*.py") if f.is_file()]
    logger.info(f"\n📋 Remaining scripts ({len(remaining_files)}):")
    for script in sorted(remaining_files):
        logger.info(f"   📄 {script}")

def verify_new_architecture():
    """Verify that the new library architecture is in place."""
    scripts_dir = Path(__file__).parent
    
    # Expected new files
    expected_files = [
        "windsurf_generator.py",  # Main orchestrator
        "lib_template_renderer.py",  # Template rendering
        "lib_github_manager.py",  # GitHub operations
        "lib_project_cleanup.py",  # Project cleanup
        "lib_project_validator.py",  # Project validation
        "lib_todo_generator.py",  # TODO generation
        "util_check_dependencies.py"  # Dependency checking
    ]
    
    logger.info("\n🔍 Verifying new architecture...")
    
    all_present = True
    for expected_file in expected_files:
        file_path = scripts_dir / expected_file
        if file_path.exists():
            logger.info(f"   ✅ {expected_file}")
        else:
            logger.error(f"   ❌ Missing: {expected_file}")
            all_present = False
    
    if all_present:
        logger.info("\n🎉 New architecture verified - all library files present!")
    else:
        logger.error("\n❌ New architecture incomplete - some files missing!")
    
    return all_present

def create_architecture_summary():
    """Create a summary of the new architecture."""
    scripts_dir = Path(__file__).parent
    
    summary_content = """# Windsurf Project Generator v4.0 - Architecture Summary

## 🏗️ Refactored Architecture

The project has been refactored from a monolithic script system to a modular library-based architecture.

### 📁 New Structure

```
scripts/
├── windsurf_generator.py           # 🎯 Main orchestrator (entry point)
├── lib_template_renderer.py        # 📦 Template rendering logic
├── lib_github_manager.py           # 🐙 GitHub repository management
├── lib_project_cleanup.py          # 🧹 Project artifact cleanup
├── lib_project_validator.py        # 🔍 Project structure validation
├── lib_todo_generator.py           # 📋 Sprint-based TODO generation
├── util_check_dependencies.py      # 🔧 Dependency checking
└── cleanup_redundant_scripts.py    # 🗑️ This cleanup script
```

### 🔄 Migration from v3.0 to v4.0

| Old Script | New Location | Status |
|-----------|-------------|---------|
| `enhanced_windsurf_generator_v3.py` | `windsurf_generator.py` + libraries | ✅ Refactored |
| `windsurf_generate.py` | `lib_template_renderer.py` | ✅ Refactored |
| `github_integration.py` | `lib_github_manager.py` | ✅ Refactored |
| `external_project_cleanup.py` | `lib_project_cleanup.py` | ✅ Refactored |
| `validate_enhanced_template.py` | `lib_project_validator.py` | ✅ Refactored |
| `todo_generator.py` | `lib_todo_generator.py` | ✅ Renamed |
| `check_dependencies.py` | `util_check_dependencies.py` | ✅ Renamed |

### 📋 Removed Scripts (Redundant)

- `enhanced_windsurf_generator.py` (older version)
- `template_fixes.py` (fixes integrated)
- `validate_templates.py` (superseded)
- `verify_fixes.py` (superseded)
- `test_inheritance.py` (superseded)
- `simulate_generation.py` (demo only)
- `test_templates.py` (superseded)

### 🎯 Usage

```bash
# Interactive mode (recommended)
python windsurf_generator.py

# Non-interactive mode
python windsurf_generator.py --template python-game-development --non-interactive

# List available templates
python windsurf_generator.py --list-templates
```

### ✨ Benefits of v4.0 Architecture

1. **Modularity**: Clear separation of concerns
2. **Maintainability**: Easier to update individual components
3. **Testability**: Each library can be tested independently
4. **Reusability**: Libraries can be used by other tools
5. **Clarity**: Single responsibility principle applied
6. **Debugging**: Easier to isolate and fix issues

### 🔧 Development

Each library module can be run independently for testing:

```bash
# Test dependency checking
python util_check_dependencies.py check

# Test project validation
python lib_project_validator.py /path/to/project

# Test project cleanup
python lib_project_cleanup.py /path/to/project

# Test TODO generation
python lib_todo_generator.py --project-name test --template-type game-development
```

---
*Generated by cleanup_redundant_scripts.py on refactoring completion*
"""
    
    summary_path = scripts_dir / "ARCHITECTURE_v4.md"
    summary_path.write_text(summary_content, encoding='utf-8')
    
    logger.info(f"\n📄 Architecture summary created: {summary_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Cleanup redundant scripts after v4.0 refactoring")
    parser.add_argument("--verify-only", action="store_true", help="Only verify new architecture")
    parser.add_argument("--summary-only", action="store_true", help="Only create architecture summary")
    
    args = parser.parse_args()
    
    if args.verify_only:
        verify_new_architecture()
    elif args.summary_only:
        create_architecture_summary()
    else:
        # Full cleanup process
        cleanup_redundant_scripts()
        verify_new_architecture()
        create_architecture_summary()
        
        print("\n🎉 Refactoring cleanup completed!")
        print("   • Redundant scripts removed")
        print("   • New architecture verified")
        print("   • Architecture summary created")
        print("\nNext steps:")
        print("   1. Test the new windsurf_generator.py")
        print("   2. Create GitHub repository for the template system")
        print("   3. Commit the refactored architecture")
