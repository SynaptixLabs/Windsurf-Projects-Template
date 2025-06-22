#!/usr/bin/env python3
"""
Git Setup Validator - Test Git operations independently
"""
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

def test_git_operations(test_dir: Path) -> bool:
    """Test Git operations in isolation."""
    print(f"🔧 Testing Git operations in: {test_dir}")
    
    try:
        # Test 1: Git init
        print("1️⃣ Testing git init...")
        subprocess.run(["git", "init"], cwd=test_dir, check=True, capture_output=True)
        print("✅ Git init successful")
        
        # Test 2: Git config
        print("2️⃣ Testing git config...")
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=test_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=test_dir, check=True)
        print("✅ Git config successful")
        
        # Test 3: Create test file and add
        print("3️⃣ Testing git add...")
        test_file = test_dir / "test.txt"
        test_file.write_text("Test content")
        subprocess.run(["git", "add", "."], cwd=test_dir, check=True, capture_output=True)
        print("✅ Git add successful")
        
        # Test 4: Commit
        print("4️⃣ Testing git commit...")
        subprocess.run(
            ["git", "commit", "-m", "Test commit"], 
            cwd=test_dir, 
            check=True, 
            capture_output=True
        )
        print("✅ Git commit successful")
        
        # Test 5: Remote operations (dry run)
        print("5️⃣ Testing git remote...")
        subprocess.run(
            ["git", "remote", "add", "origin", "git@github.com:test/test.git"], 
            cwd=test_dir, 
            check=True, 
            capture_output=True
        )
        print("✅ Git remote add successful")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        print(f"Command: {e.cmd}")
        if e.stderr:
            print(f"Error: {e.stderr.decode()}")
        return False

def main():
    """Run Git validation tests."""
    print("🧪 Git Operations Validator")
    print("=" * 50)
    
    # Create temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        test_path = Path(temp_dir) / "git_test"
        test_path.mkdir()
        
        success = test_git_operations(test_path)
        
        if success:
            print("\n🎉 All Git operations successful!")
            print("✅ Git setup should work properly")
            return 0
        else:
            print("\n❌ Git operations failed!")
            print("🔧 Check your Git installation and PATH")
            return 1

if __name__ == "__main__":
    sys.exit(main())
