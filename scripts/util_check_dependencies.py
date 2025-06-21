#!/usr/bin/env python3
"""
Dependency Checker Utility

Checks for required dependencies before running the Windsurf project generator.
Renamed from check_dependencies.py to follow utility naming convention.
"""

import sys
import subprocess
import logging
from typing import List, Tuple, Dict, Any
from pathlib import Path


class DependencyChecker:
    """Checks for required dependencies and system requirements."""
    
    def __init__(self):
        self.logger = logging.getLogger('dependency_checker')
        self.required_python_version = (3, 9)
        self.required_packages = [
            'copier',
            'pydantic',
            'requests'  # Optional but recommended for GitHub API
        ]
        self.optional_packages = [
            'tomllib',  # For TOML validation (Python 3.11+)
            'yaml'      # For YAML handling
        ]
    
    def check_all_dependencies(self) -> bool:
        """
        Check all dependencies and system requirements.
        
        Returns:
            True if all requirements are met, False otherwise
        """
        self.logger.info("🔍 Checking system dependencies...")
        
        checks = [
            ("Python Version", self._check_python_version),
            ("Required Packages", self._check_required_packages),
            ("Git Installation", self._check_git_available),
            ("Project Structure", self._check_project_structure)
        ]
        
        all_passed = True
        results = []
        
        for check_name, check_func in checks:
            try:
                success, message = check_func()
                results.append((check_name, success, message))
                
                if success:
                    self.logger.info(f"✅ {check_name}: {message}")
                else:
                    self.logger.error(f"❌ {check_name}: {message}")
                    all_passed = False
                    
            except Exception as e:
                self.logger.error(f"❌ {check_name}: Error during check - {e}")
                all_passed = False
        
        # Check optional packages (warnings only)
        self._check_optional_packages()
        
        if all_passed:
            self.logger.info("✅ All dependency checks passed")
        else:
            self.logger.error("❌ Some dependency checks failed")
            self._provide_installation_help(results)
        
        return all_passed
    
    def _check_python_version(self) -> Tuple[bool, str]:
        """Check Python version meets requirements."""
        current_version = sys.version_info[:2]
        required_version = self.required_python_version
        
        if current_version >= required_version:
            return True, f"Python {'.'.join(map(str, current_version))} (required: {'.'.join(map(str, required_version))}+)"
        else:
            return False, f"Python {'.'.join(map(str, current_version))} insufficient (required: {'.'.join(map(str, required_version))}+)"
    
    def _check_required_packages(self) -> Tuple[bool, str]:
        """Check required Python packages are installed."""
        missing_packages = []
        
        for package in self.required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if not missing_packages:
            return True, f"All required packages available ({', '.join(self.required_packages)})"
        else:
            return False, f"Missing packages: {', '.join(missing_packages)}"
    
    def _check_optional_packages(self) -> None:
        """Check optional packages and provide info warnings."""
        for package in self.optional_packages:
            try:
                __import__(package)
                self.logger.debug(f"✅ Optional package available: {package}")
            except ImportError:
                self.logger.debug(f"ℹ️ Optional package not available: {package}")
    
    def _check_git_available(self) -> Tuple[bool, str]:
        """Check if Git is available."""
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                version_info = result.stdout.strip()
                return True, f"Git available ({version_info})"
            else:
                return False, "Git command failed"
                
        except FileNotFoundError:
            return False, "Git not found in PATH"
        except Exception as e:
            return False, f"Git check error: {e}"
    
    def _check_project_structure(self) -> Tuple[bool, str]:
        """Check that we're running from the correct project structure."""
        script_dir = Path(__file__).parent
        template_generators_dir = script_dir.parent / "template-generators"
        
        if not template_generators_dir.exists():
            return False, f"template-generators directory not found at {template_generators_dir}"
        
        # Check for at least one template
        templates = [d for d in template_generators_dir.iterdir() 
                    if d.is_dir() and not d.name.startswith('.')]
        
        if not templates:
            return False, "No template directories found in template-generators/"
        
        return True, f"Project structure valid ({len(templates)} templates available)"
    
    def _provide_installation_help(self, results: List[Tuple[str, bool, str]]) -> None:
        """Provide installation help for failed checks."""
        self.logger.error("\n💡 Installation Help:")
        
        for check_name, success, message in results:
            if not success:
                if check_name == "Python Version":
                    self.logger.error("   • Install Python 3.9+ from https://python.org")
                elif check_name == "Required Packages":
                    self.logger.error("   • Install missing packages:")
                    self.logger.error("     pip install copier pydantic requests")
                    self.logger.error("     # OR using poetry:")
                    self.logger.error("     poetry add copier pydantic requests")
                elif check_name == "Git Installation":
                    self.logger.error("   • Install Git from https://git-scm.com")
                elif check_name == "Project Structure":
                    self.logger.error("   • Ensure you're running from the Windsurf-Projects-Template directory")
                    self.logger.error("   • Check that template-generators/ directory exists")


if __name__ == "__main__":
    # Test functionality
    import argparse
    
    parser = argparse.ArgumentParser(description="Dependency Checker")
    parser.add_argument("command", 
                       choices=["check", "install"],
                       help="Command to run")
    parser.add_argument("--package", help="Check specific package")
    
    args = parser.parse_args()
    
    checker = DependencyChecker()
    
    if args.command == "check":
        success = checker.check_all_dependencies()
        sys.exit(0 if success else 1)
    elif args.command == "install":
        print("Auto-installation not implemented. Please install manually:")
        print("pip install copier pydantic requests")
