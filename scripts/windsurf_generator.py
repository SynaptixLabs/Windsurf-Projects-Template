#!/usr/bin/env python3
"""
Windsurf Python Project Generator - Main Orchestrator

This is the main entry point for the Windsurf project template system.
It orchestrates all other library modules to provide a clean, maintainable
project generation workflow.

Version: 5.4 (FIXED: Cleanup Order & Re-enabled Cleanup)
"""

import sys
import argparse
import logging
import datetime
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

# Add the script's parent directory to the Python path to allow direct execution.
# This reverts the need for 'poetry run' by making the library modules findable.
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(script_dir))

# Import our library modules
from lib_template_renderer import TemplateRenderer
from lib_github_manager import GitHubManager
from lib_project_cleanup import ProjectCleaner
from lib_project_validator import ProjectValidator
from lib_todo_generator import TODOGenerator
from util_check_dependencies import DependencyChecker


class WindsurfGenerator:
    """Main orchestrator for Windsurf project generation."""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.template_renderer = TemplateRenderer()
        self.github_manager = GitHubManager()
        self.project_cleaner = ProjectCleaner()
        self.project_validator = ProjectValidator()
        self.todo_generator = TODOGenerator()
        self.dependency_checker = DependencyChecker()
    
    def _setup_logging(self) -> logging.Logger:
        logger_name = 'windsurf_generator'
        logger = logging.getLogger(logger_name)
        
        if logger.hasHandlers():
            return logger
        
        logger.setLevel(logging.DEBUG)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        try:
            logs_dir = Path.cwd() / "logs"
            logs_dir.mkdir(exist_ok=True)
            import uuid
            session_uuid = str(uuid.uuid4())[:8]
            log_file = logs_dir / f"project_generator_{session_uuid}.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            detailed_formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)
            
            logger.info(f"📝 Unified log file: {log_file}")
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")

        logger.info("=" * 80)
        logger.info("🚀 WINDSURF PROJECT GENERATOR v5.4 'CLEANUP-FIXED'")
        logger.info(f"🕐 Session started: {datetime.datetime.now()}")
        logger.info("=" * 80)
        
        return logger
    
    def generate_project(
        self,
        template: Optional[str] = None,
        interactive: bool = True,
        project_dir: Optional[Path] = None,
        **kwargs
    ) -> bool:
        """
        Main project generation workflow with CORRECTED order of operations.
        """
        self.logger.info("🚀 Starting Windsurf project generation v5.4 'Cleanup-Fixed'")

        # Step 0: Check for required system dependencies
        self.logger.info("🔍 PHASE START: Verifying system dependencies...")
        if not self.dependency_checker.check_all_dependencies():
            self.logger.error("❌ Critical dependencies are missing. Please install them before proceeding.")
            return False
        self.logger.info("✅ PHASE END: System dependencies verified.")

        try:
            # Step 1: Establish target directory and get configuration
            if project_dir:
                target_dir = Path(project_dir).resolve()
            else:
                target_dir = Path.cwd().resolve()
            target_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"📁 Project will be generated in: {target_dir}")

            config = self._get_project_configuration(template, interactive, target_dir, **kwargs)
            if not config:
                self.logger.error("❌ Project configuration failed.")
                return False
            
            # --- CORE WORKFLOW (Corrected Order) ---
            # 1. Render the project template
            self.logger.info("PHASE 1: Rendering project templates...")
            final_answers = self.template_renderer.render_project(config)
            if not final_answers:
                self.logger.error("❌ Template rendering failed.")
                return False
            config.update(final_answers)
            self.logger.info("✅ PHASE 1 COMPLETE.")

            # 2. Run post-generation installer (uses .copier-answers.yml)
            self.logger.info("PHASE 2: Running post-generation installer...")
            installer_success = self._run_post_generation_installer(target_dir)
            if not installer_success:
                self.logger.error("❌ Post-generation installation failed. The project may be in an incomplete state.")
                return False # Fail fast if installation fails
            self.logger.info("✅ PHASE 2 COMPLETE.")

            # 3. Clean up artifacts (removes .copier-answers.yml)
            self.logger.info("PHASE 3: Cleaning up temporary artifacts...")
            self.project_cleaner.cleanup_project(target_dir)
            self.logger.info("✅ PHASE 3 COMPLETE.")

            # 4. Create GitHub repository if requested
            self.logger.info("PHASE 4: Setting up GitHub repository...")
            if config.get('create_github_repo'):
                repo_url = self.github_manager.create_repository(
                    project_name=config['project_name'],
                    description=config['project_description'],
                    project_dir=target_dir,
                    org=config.get('github_org', 'SynaptixLabs'),
                    private=config.get('github_private', False),
                    auto_commit=True
                )
                if repo_url:
                    config['github_url'] = repo_url
                    self.logger.info(f"✅ GitHub repository setup completed: {repo_url}")
                else:
                    self.logger.warning("⚠️ Failed to create GitHub repository.")
            self.logger.info("✅ PHASE 4 COMPLETE.")

            # 5. Validate the final project state (verifies .copier-answers.yml is gone)
            self.logger.info("PHASE 5: Validating final project state...")
            self._validate_project_with_report(target_dir, config)
            self.logger.info("✅ PHASE 5 COMPLETE.")

            # 6. Generate TODO lists
            self.logger.info("PHASE 6: Generating TODO lists...")
            self._generate_todo_lists(target_dir, config)
            self.logger.info("✅ PHASE 6 COMPLETE.")

            # --- FINAL SUMMARY ---
            self._display_success_summary(config)
            return True

        except Exception as e:
            self.logger.error(f"❌ Project generation failed with a critical error: {e}")
            import traceback
            self.logger.debug(f"Full error traceback:\n{traceback.format_exc()}")
            return False

    def _get_project_configuration(self, template, interactive, target_dir, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Gets project configuration. In interactive mode, this now fully delegates
        to Copier by passing it no data. In non-interactive mode, it uses defaults.
        The template can be provided via menu or command-line argument.
        """
        available_templates = self.template_renderer.get_available_templates()
        
        if template is None and interactive:
            template = self._display_template_menu(available_templates)
        elif template is None: # Non-interactive mode
            self.logger.error("Template must be specified in non-interactive mode via the --template argument.")
            return None
        
        if template not in available_templates:
            self.logger.error(f"Template '{template}' not found.")
            return None
        
        # REVERTED: Pre-fill project data to provide sensible defaults in interactive mode.
        # This allows Copier to suggest defaults instead of forcing user input.
        if interactive:
            project_data = self._get_default_project_data(target_dir)
            github_config = {}
        else:
            # Non-interactive mode requires pre-filled defaults.
            project_data = self._get_default_project_data(target_dir)
            # Add defaults for non-interactive mode to avoid prompts
            project_data['complexity_preset'] = 'Intermediate'
            project_data['integration_focus'] = 'ai_first'
            github_config = {
                'create_github_repo': True,
                'github_private': True,
                'github_org': 'SynaptixLabs'
            }

        return {
            'template': template, 
            'template_info': available_templates[template], 
            'target_dir': target_dir, 
            'interactive': interactive, 
            **project_data, 
            **github_config, 
            **kwargs
        }

    def _display_template_menu(self, templates: Dict[str, Any]) -> Optional[str]:
        print("\n🎯 Windsurf Python Project Generator v5.4")
        print("=" * 50)
        template_list = list(templates.items())
        for i, (name, info) in enumerate(template_list, 1):
            print(f"{i}. {name}: {info['description']}")
        while True:
            try:
                choice = int(input(f"Enter your choice (1-{len(template_list)}): "))
                if 1 <= choice <= len(template_list):
                    return template_list[choice - 1][0]
            except (ValueError, IndexError):
                print("Invalid choice.")

    def _get_default_project_data(self, target_dir: Path) -> Dict[str, Any]:
        return {'project_name': target_dir.name, 'project_description': f"A new project: {target_dir.name}", 'author_name': 'Avidor', 'author_email': 'avidor@synaptixlabs.ai', 'python_version': '3.12'}

    def _generate_todo_lists(self, target_dir: Path, config: Dict[str, Any]) -> None:
        try:
            template_type = config['template'].replace('python-', '')
            for sprint in range(1, 5):
                self.todo_generator.generate_todo_file(project_name=config['project_name'], template_type=template_type, sprint_number=sprint, output_dir=target_dir / 'docs')
        except Exception as e:
            self.logger.warning(f"TODO generation failed: {e}")
    
    def _validate_project_with_report(self, target_dir: Path, config: Dict[str, Any]) -> None:
        """
        Enhanced validation that specifically checks for template cleanup success.
        """
        try:
            logs_dir = target_dir / "logs"
            logs_dir.mkdir(exist_ok=True)

            # Specific check for copier answers file (should NOT exist after cleanup)
            copier_answers_file = target_dir / ".copier-answers.yml"
            if copier_answers_file.exists():
                self.logger.error(f"❌ CRITICAL: Copier answers file still exists at {copier_answers_file}")
                self.logger.error("❌ This indicates cleanup failed and template artifacts were committed!")
            else:
                self.logger.info("✅ Copier answers file successfully removed.")

            # Run full validation
            validation_success = self.project_validator.validate_project(target_dir, project_config=config)
            if not validation_success:
                self.logger.warning("⚠️ Project validation found issues.")
            else:
                self.logger.info("✅ Project validation passed all checks.")

            # Move validation report
            validation_report_src = target_dir / "validation_report.md"
            if validation_report_src.exists():
                validation_report_dest = logs_dir / "validation_report.md"
                validation_report_src.rename(validation_report_dest)
                self.logger.info(f"📋 Validation report moved to: {validation_report_dest}")

        except Exception as e:
            self.logger.warning(f"Validation failed: {e}")

    def _run_post_generation_installer(self, target_dir: Path) -> bool:
        """
        Runs the framework installation script after project generation.
        This is now called explicitly to avoid race conditions with copier tasks.
        """
        # The installer script is part of the python-modern template generator
        installer_script_path = (
            Path(__file__).parent.parent
            / "template-generators"
            / "python-modern"
            / "scripts"
            / "install_frameworks.py"
        )

        if not installer_script_path.exists():
            self.logger.warning(f"Installer script not found at {installer_script_path}. Skipping installation.")
            return False

        # Use sys.executable to ensure we're using the same Python interpreter
        command = [sys.executable, "-B", str(installer_script_path)]
        
        self.logger.info(f"Executing installer command: {' '.join(command)}")
        self.logger.info(f"Working directory: {target_dir}")

        try:
            # Run the installer script with the project's root as the CWD.
            # The installer script is designed to find the .copier-answers.yml in its CWD.
            result = subprocess.run(
                command,
                cwd=target_dir,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',  # Add this line to prevent UnicodeDecodeError
                check=False  # We check the returncode manually to provide better logging
            )

            if result.returncode == 0:
                self.logger.info("--- Installer Script Output ---")
                self.logger.info(result.stdout)
                self.logger.info("-----------------------------")
                return True
            else:
                self.logger.error("❌ Post-generation installer script failed!")
                self.logger.error(f"Return Code: {result.returncode}")
                self.logger.error("--- Installer Script STDOUT ---")
                self.logger.error(result.stdout)
                self.logger.error("--- Installer Script STDERR ---")
                self.logger.error(result.stderr)
                self.logger.error("-----------------------------")
                return False
        except FileNotFoundError:
            self.logger.error(f"❌ Installer script not found at path: {installer_script_path}")
            return False
        except Exception as e:
            self.logger.error(f"❌ An unexpected error occurred while running the installer script: {e}")
            import traceback
            self.logger.debug(f"Full error traceback:\n{traceback.format_exc()}")
            return False

    def _display_success_summary(self, config: Dict[str, Any]) -> None:
        github_info = f"\nGitHub: {config['github_url']}" if config.get('github_url') else "\nGitHub: Not created."
        summary = f"""
[SUCCESS] Project '{config['project_name']}' Generated Successfully!

   Template: {config['template']}
   Location: {config['target_dir']}{github_info}

Next Steps:
   1. cd {config['target_dir']}
   2. poetry install
   3. poetry run pre-commit install
   4. poetry run test
   5. Start developing in the src/ directory!

Happy coding!
"""
        print(summary)
        self.logger.info("WINDSURF PROJECT GENERATOR SESSION COMPLETED")

def main():
    parser = argparse.ArgumentParser(description="Windsurf Python Project Generator v5.4")
    parser.add_argument(
        "project_dir", 
        nargs='?', 
        default=None, 
        type=Path, 
        help="Target directory for project generation. Defaults to current directory."
    )
    parser.add_argument("--template", help="Template type to use (e.g., 'python-modern')")
    parser.add_argument("--non-interactive", action="store_true", help="Run with minimal prompts")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode (default). This flag is ignored.")
    
    args = parser.parse_args()
    
    generator = WindsurfGenerator()

    # --- DEPENDENCY CHECK ---
    # Ensure all required dependencies are met before proceeding.
    if not generator.dependency_checker.check_all_dependencies():
        generator.logger.error("Dependency checks failed. Please install the required dependencies and try again.")
        sys.exit(1)

    success = generator.generate_project(
        template=args.template,
        interactive=not args.non_interactive,
        project_dir=args.project_dir
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()