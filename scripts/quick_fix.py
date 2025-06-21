#!/usr/bin/env python3
"""
Quick Fix Script - Fix Git Issues and Push
"""

import subprocess
import os
from pathlib import Path

def run_cmd(cmd, description, check=False):
    """Run command with logging."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                              cwd="C:/Synaptix-Labs/projects/Windsurf-Projects-Template")
        if result.returncode == 0:
            print(f"✅ {description} completed")
        else:
            print(f"⚠️ {description}: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def quick_fix():
    """Quick fix for git issues."""
    print("🛠️ Quick Fix: Git Issues and Push")
    print("=" * 50)
    
    project_root = Path("C:/Synaptix-Labs/projects/Windsurf-Projects-Template")
    scripts_dir = project_root / "scripts"
    
    # Step 1: Manual cleanup of redundant files
    print("🧹 Step 1: Manual cleanup...")
    redundant_files = [
        "enhanced_windsurf_generator.py",
        "windsurf_generate.py", 
        "github_integration.py",
        "external_project_cleanup.py",
        "todo_generator.py",
        "check_dependencies.py",
        "enhanced_windsurf_generator_v3.py",
        "template_fixes.py",
        "validate_templates.py",
        "verify_fixes.py",
        "test_templates.py",
        "simulate_generation.py",
        "validate_enhanced_template.py",
        "generate_project.py"
    ]
    
    for file_name in redundant_files:
        file_path = scripts_dir / file_name
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"   ✅ Removed: {file_name}")
            except Exception as e:
                print(f"   ❌ Failed to remove {file_name}: {e}")
    
    # Step 2: Fix remote URL (switch from SSH to HTTPS)
    print("\n🔗 Step 2: Fixing remote URL...")
    run_cmd("git remote remove origin", "Removing old remote", check=False)
    run_cmd("git remote add origin https://github.com/SynaptixLabs/Windsurf-Projects-Template.git", "Adding HTTPS remote")
    
    # Step 3: Ensure we're on a branch
    print("\n🌿 Step 3: Ensuring branch exists...")
    run_cmd("git checkout -b main", "Creating main branch", check=False)
    
    # Step 4: Stage and commit
    print("\n📦 Step 4: Staging and committing...")
    run_cmd("git add .", "Staging files")
    run_cmd('git commit -m "🎉 Windsurf Project Template Generator v4.0 - Refactored modular architecture"', "Creating commit")
    
    # Step 5: Push to remote
    print("\n🚀 Step 5: Pushing to remote...")
    if not run_cmd("git push -u origin main", "Pushing to main"):
        run_cmd("git push -u origin master", "Trying master branch")
    
    # Step 6: Verify
    print("\n✅ Step 6: Verification...")
    run_cmd("git remote -v", "Checking remote")
    run_cmd("git log --oneline -3", "Checking commits")
    
    print("\n🎉 Quick fix completed! Check your GitHub repository.")

if __name__ == "__main__":
    quick_fix()
