#!/usr/bin/env python3
"""
Diagnostic Script - Check Git Status and Fix Issues
"""

import subprocess
import os

def run_git_command(cmd, description):
    """Run git command and show output."""
    print(f"\n🔍 {description}:")
    print("-" * 50)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="C:/Synaptix-Labs/projects/Windsurf-Projects-Template")
        print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        print(f"Return code: {result.returncode}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("🔍 Git Repository Diagnostic")
    print("=" * 50)
    
    # Check current branch
    run_git_command("git branch", "Current branches")
    
    # Check git status  
    run_git_command("git status", "Git status")
    
    # Check remote configuration
    run_git_command("git remote -v", "Remote configuration")
    
    # Check if we have any commits
    run_git_command("git log --oneline -5", "Recent commits")
    
    # Check current branch name
    run_git_command("git rev-parse --abbrev-ref HEAD", "Current branch name")
