#!/usr/bin/env python3
"""
Project Validator Library

Handles validation of generated project structure and integrity.
Consolidated from validate_enhanced_template.py and test_templates.py.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import re


class ProjectValidator:
    """Validates generated project structure and integrity."""
    
    def __init__(self):
        self.logger = logging.getLogger('project_validator')
        
        # Essential files that should exist in a Python project
        self.essential_files = [
            'pyproject.toml',
            'README.md',
            '.gitignore'
        ]
        
        # Essential directories for modern Python projects
        self.essential_directories = [
            'src',
            'tests',
            'docs'
        ]
        
        # Files that should NOT exist (template artifacts)
        self.forbidden_files = [
            'copier-answers.yml',
            '.copier-answers.yml'
        ]
        
        # Directories that should NOT exist (template artifacts)
        self.forbidden_directories = [
            'template',
            'template_DELETE_ME'
        ]
        
        # Patterns that should NOT exist
        self.forbidden_patterns = [
            r'.*\.DISABLE.*',
            r'.*\.jinja\.bak.*',
            r'.*DELETE_ME.*'
        ]
    
    def validate_project(self, project_dir: Path, project_config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate the entire project structure.
        
        Args:
            project_dir: Path to the project directory
            
        Returns:
            True if validation passes, False otherwise
        """
        try:
            self.logger.info(f"🔍 Validating project structure: {project_dir}")
            
            validation_results = []
            
            # Run all validation checks
            checks = [
                ("Essential Files", self._check_essential_files),
                ("Essential Directories", self._check_essential_directories),
                ("Forbidden Artifacts", self._check_forbidden_artifacts),
                ("Python Package Structure", self._check_python_package_structure),
                ("Configuration Files", self._check_configuration_files),
                ("Documentation Structure", self._check_documentation_structure),
                ("Testing Structure", self._check_testing_structure),
                ("Git Repository", self._check_git_repository)  # NEW: Git validation
            ]
            
            all_passed = True
            
            for check_name, check_func in checks:
                try:
                    # Pass config to the git check only
                    if check_name == "Git Repository":
                        success, details = check_func(project_dir, project_config=project_config)
                    else:
                        success, details = check_func(project_dir)
                        
                    validation_results.append((check_name, success, details))
                    
                    if success:
                        self.logger.info(f"✅ {check_name}: {details}")
                    else:
                        self.logger.warning(f"⚠️ {check_name}: {details}")
                        all_passed = False
                        
                except Exception as e:
                    self.logger.error(f"❌ {check_name}: Validation error - {e}")
                    all_passed = False
            
            # Generate validation report
            self._generate_validation_report(project_dir, validation_results)
            
            if all_passed:
                self.logger.info("✅ Project validation passed - all checks successful!")
            else:
                self.logger.warning("⚠️ Project validation completed with warnings")
            
            return all_passed
            
        except Exception as e:
            self.logger.error(f"❌ Project validation failed: {e}")
            return False
    
    def _check_essential_files(self, project_dir: Path) -> Tuple[bool, str]:
        """Check that essential files exist."""
        missing_files = []
        
        for file_name in self.essential_files:
            file_path = project_dir / file_name
            if not file_path.exists():
                missing_files.append(file_name)
        
        if missing_files:
            return False, f"Missing essential files: {', '.join(missing_files)}"
        else:
            return True, f"All essential files present ({len(self.essential_files)} files)"
    
    def _check_essential_directories(self, project_dir: Path) -> Tuple[bool, str]:
        """Check that essential directories exist."""
        missing_dirs = []
        
        for dir_name in self.essential_directories:
            dir_path = project_dir / dir_name
            if not dir_path.exists() or not dir_path.is_dir():
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            return False, f"Missing essential directories: {', '.join(missing_dirs)}"
        else:
            return True, f"All essential directories present ({len(self.essential_directories)} directories)"
    
    def _check_forbidden_artifacts(self, project_dir: Path) -> Tuple[bool, str]:
        """Check for template artifacts that should not exist."""
        artifacts_found = []
        
        # Check forbidden files
        for file_name in self.forbidden_files:
            for artifact_file in project_dir.rglob(file_name):
                if artifact_file.is_file():
                    artifacts_found.append(str(artifact_file.relative_to(project_dir)))
        
        # Check forbidden directories
        for dir_name in self.forbidden_directories:
            for artifact_dir in project_dir.rglob(dir_name):
                if artifact_dir.is_dir():
                    artifacts_found.append(f"{artifact_dir.relative_to(project_dir)}/")
        
        # Check forbidden patterns
        for pattern in self.forbidden_patterns:
            regex = re.compile(pattern)
            for item in project_dir.rglob("*"):
                if regex.match(item.name):
                    artifacts_found.append(str(item.relative_to(project_dir)))
        
        if artifacts_found:
            return False, f"Template artifacts found: {', '.join(artifacts_found[:5])}"
        else:
            return True, "No template artifacts found"
    
    def _check_python_package_structure(self, project_dir: Path) -> Tuple[bool, str]:
        """Check Python package structure in src/ directory."""
        src_dir = project_dir / "src"
        
        if not src_dir.exists():
            return False, "src/ directory not found"
        
        # Look for Python package directories
        package_dirs = [d for d in src_dir.iterdir() 
                       if d.is_dir() and not d.name.startswith('.') and not d.name.startswith('__')]
        
        if not package_dirs:
            return False, "No Python package found in src/"
        
        # Check each package for __init__.py
        packages_with_init = []
        for package_dir in package_dirs:
            init_file = package_dir / "__init__.py"
            if init_file.exists():
                packages_with_init.append(package_dir.name)
        
        if not packages_with_init:
            return False, f"No packages with __init__.py found in src/ (found directories: {[d.name for d in package_dirs]})"
        
        return True, f"Valid Python packages found: {', '.join(packages_with_init)}"
    
    def _check_configuration_files(self, project_dir: Path) -> Tuple[bool, str]:
        """Check configuration files are valid."""
        config_issues = []
        
        # Check pyproject.toml
        pyproject_file = project_dir / "pyproject.toml"
        if pyproject_file.exists():
            try:
                import tomllib
                content = pyproject_file.read_text(encoding='utf-8')
                tomllib.loads(content)
            except ImportError:
                # Python < 3.11, try tomli or skip
                try:
                    import tomli
                    content = pyproject_file.read_text(encoding='utf-8')
                    tomli.loads(content)
                except ImportError:
                    pass  # Skip validation if no TOML library available
            except Exception as e:
                config_issues.append(f"pyproject.toml invalid: {e}")
        
        # Check for common config files and basic validation
        config_files = {
            'ruff.toml': 'TOML',
            'mypy.ini': 'INI',
            'pytest.ini': 'INI',
            '.pre-commit-config.yaml': 'YAML'
        }
        
        valid_configs = []
        for config_file, file_type in config_files.items():
            config_path = project_dir / config_file
            if config_path.exists():
                try:
                    # Basic validation - just try to read
                    content = config_path.read_text(encoding='utf-8')
                    if content.strip():  # Not empty
                        valid_configs.append(config_file)
                except Exception as e:
                    config_issues.append(f"{config_file} invalid: {e}")
        
        if config_issues:
            return False, f"Configuration issues: {'; '.join(config_issues)}"
        else:
            return True, f"Configuration files valid ({len(valid_configs)} config files found)"
    
    def _check_documentation_structure(self, project_dir: Path) -> Tuple[bool, str]:
        """Check documentation structure."""
        docs_dir = project_dir / "docs"
        
        if not docs_dir.exists():
            return False, "docs/ directory not found"
        
        # Look for documentation files
        doc_files = []
        windsurf_files = []
        
        for file_path in docs_dir.rglob("*.md"):
            doc_files.append(file_path.name)
            
            # Check for Windsurf-specific documentation
            if any(windsurf_term in file_path.name.lower() 
                   for windsurf_term in ['roadmap', 'summary', 'techstack', 'status', 'todo']):
                windsurf_files.append(file_path.name)
        
        if not doc_files:
            return False, "No documentation files found in docs/"
        
        status_info = f"{len(doc_files)} documentation files"
        if windsurf_files:
            status_info += f", {len(windsurf_files)} Windsurf integration files"
        
        return True, status_info
    
    def _check_testing_structure(self, project_dir: Path) -> Tuple[bool, str]:
        """Check testing structure."""
        tests_dir = project_dir / "tests"
        
        if not tests_dir.exists():
            return False, "tests/ directory not found"
        
        # Look for test files
        test_files = list(tests_dir.rglob("test_*.py")) + list(tests_dir.rglob("*_test.py"))
        
        # Look for test configuration
        config_files = []
        for config_file in ['conftest.py', 'pytest.ini', '.pytest.ini']:
            if (tests_dir / config_file).exists() or (project_dir / config_file).exists():
                config_files.append(config_file)
        
        if not test_files and not config_files:
            return False, "No test files or configuration found"
        
        status_info = f"{len(test_files)} test files"
        if config_files:
            status_info += f", test configuration present"
        
        return True, status_info
    
    def _check_git_repository(self, project_dir: Path, project_config: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Check Git repository status and configuration."""
        # If config is provided and user opted out of repo creation, it's not an error.
        if project_config and not project_config.get('create_github_repo', False):
            return True, "Git repository creation was skipped by user choice."

        import subprocess
        
        issues = []
        git_status = {
            'initialized': False,
            'has_commits': False,
            'has_remote': False,
            'remote_url': None
        }
        
        # Check if git is initialized
        git_dir = project_dir / ".git"
        if not git_dir.exists():
            issues.append("Git repository not initialized")
        else:
            git_status['initialized'] = True
            
            try:
                # Check for commits (explicit cwd)
                result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                                      cwd=project_dir, capture_output=True, 
                                      text=True, check=False)
                if result.returncode == 0 and result.stdout.strip():
                    git_status['has_commits'] = True
                else:
                    issues.append("No commits found")
                
                # Check for remote origin (explicit cwd)
                result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                      cwd=project_dir, capture_output=True, 
                                      text=True, check=False)
                if result.returncode == 0 and result.stdout.strip():
                    git_status['has_remote'] = True
                    git_status['remote_url'] = result.stdout.strip()
                else:
                    issues.append("No remote 'origin' configured")
                
            except Exception as e:
                issues.append(f"Git command failed: {e}")
        
        # Determine overall status
        if not issues:
            status_msg = f"Git repository properly configured"
            if git_status['remote_url']:
                # Extract repo name from URL for cleaner display
                repo_name = git_status['remote_url'].split('/')[-1].replace('.git', '')
                status_msg += f" (remote: {repo_name})"
            return True, status_msg
        else:
            return False, f"Git issues: {'; '.join(issues)}"
    
    def _generate_validation_report(self, project_dir: Path, results: List[Tuple[str, bool, str]]) -> None:
        """Generate a validation report file."""
        try:
            report_path = project_dir / "validation_report.md"
            
            report_content = f"""# Project Validation Report

**Project:** {project_dir.name}
**Validation Date:** {self._get_current_timestamp()}
**Validation Tool:** Windsurf Project Validator v4.0

## Validation Results

"""
            
            for check_name, success, details in results:
                status = "✅ PASS" if success else "⚠️ WARNING"
                report_content += f"### {check_name}\n"
                report_content += f"**Status:** {status}\n"
                report_content += f"**Details:** {details}\n\n"
            
            # Add summary
            passed_checks = sum(1 for _, success, _ in results if success)
            total_checks = len(results)
            
            report_content += f"""## Summary

- **Total Checks:** {total_checks}
- **Passed:** {passed_checks}
- **Warnings:** {total_checks - passed_checks}
- **Overall Status:** {"✅ PASS" if passed_checks == total_checks else "⚠️ WARNINGS"}

## Recommendations

"""
            
            # Add recommendations based on failed checks
            for check_name, success, details in results:
                if not success:
                    report_content += f"- **{check_name}:** {self._get_recommendation(check_name)}\n"
            
            if passed_checks == total_checks:
                report_content += "All validation checks passed! Your project structure looks good.\n"
            
            report_content += f"""
---
*Generated by Windsurf Project Template Generator v4.0*
*Report saved to: {report_path}*
"""
            
            report_path.write_text(report_content, encoding='utf-8')
            self.logger.debug(f"📄 Validation report saved: {report_path}")
            
        except Exception as e:
            self.logger.warning(f"Failed to generate validation report: {e}")
    
    def _get_recommendation(self, check_name: str) -> str:
        """Get recommendation for failed checks."""
        recommendations = {
            "Essential Files": "Create missing files using the project template or manually",
            "Essential Directories": "Create missing directories and populate with appropriate content",
            "Forbidden Artifacts": "Run project cleanup to remove template artifacts",
            "Python Package Structure": "Ensure src/ contains a proper Python package with __init__.py",
            "Configuration Files": "Fix syntax errors in configuration files",
            "Documentation Structure": "Add documentation files to docs/ directory",
            "Testing Structure": "Add test files and pytest configuration",
            "Git Repository": "Initialize git repository, make initial commit, and configure remote origin"
        }
        return recommendations.get(check_name, "Review and fix the identified issues")
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for reports."""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def validate_specific_component(self, project_dir: Path, component: str) -> bool:
        """Validate a specific component of the project."""
        component_checks = {
            'files': self._check_essential_files,
            'directories': self._check_essential_directories,
            'artifacts': self._check_forbidden_artifacts,
            'python': self._check_python_package_structure,
            'config': self._check_configuration_files,
            'docs': self._check_documentation_structure,
            'tests': self._check_testing_structure,
            'git': self._check_git_repository  # NEW: Git validation
        }
        
        if component not in component_checks:
            self.logger.error(f"Unknown component: {component}")
            return False
        
        try:
            success, details = component_checks[component](project_dir)
            status = "✅" if success else "⚠️"
            self.logger.info(f"{status} {component.title()}: {details}")
            return success
        except Exception as e:
            self.logger.error(f"❌ {component.title()} validation failed: {e}")
            return False


if __name__ == "__main__":
    # Test functionality
    import argparse
    
    parser = argparse.ArgumentParser(description="Project Validator Test")
    parser.add_argument("project_dir", type=Path, help="Project directory to validate")
    parser.add_argument("--component", choices=['files', 'directories', 'artifacts', 'python', 'config', 'docs', 'tests', 'git'],
                       help="Validate specific component only")
    
    args = parser.parse_args()
    
    validator = ProjectValidator()
    
    if args.component:
        success = validator.validate_specific_component(args.project_dir, args.component)
        print(f"{'✅' if success else '⚠️'} {args.component.title()} validation {'passed' if success else 'failed'}")
    else:
        success = validator.validate_project(args.project_dir)
        print(f"{'✅' if success else '⚠️'} Project validation {'passed' if success else 'completed with warnings'}")
