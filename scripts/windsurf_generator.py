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
from pathlib import Path
from typing import Optional, Dict, Any

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
        
        FIXED ORDER:
        1. Render templates (creates template directory)
        2. Clean up artifacts (REMOVES template directory)  
        3. Setup GitHub (commits CLEAN project)
        4. Validate (confirms template directory is gone)
        5. Generate TODOs
        """
        self.logger.info("🚀 Starting Windsurf project generation v5.4 'Cleanup-Fixed'")
        try:
            # Step 1: Establish target directory
            if project_dir:
                target_dir = Path(project_dir).resolve()
            else:
                target_dir = Path.cwd().resolve()
            
            self.logger.info(f"📁 DEFINITIVE PROJECT PATH: {target_dir}")
            target_dir.mkdir(parents=True, exist_ok=True)

            # Step 2: Get project configuration
            self.logger.debug("🔍 Getting project configuration...")
            project_config = self._get_project_configuration(template, interactive, target_dir, **kwargs)
            if not project_config:
                return False
            
            self.logger.info("📋 Project Configuration:")
            for key, value in project_config.items():
                if key != 'template_info':
                    self.logger.info(f"   {key}: {value}")

            # Step 3: Render templates
            self.logger.info("📦 PHASE START: Rendering project templates...")
            if not self.template_renderer.render_project(project_config):
                self.logger.error("❌ Template rendering failed.")
                return False
            self.logger.info("✅ PHASE END: Template rendering completed.")

            # --- CRITICAL FIX: CLEANUP BEFORE GITHUB ---

            # Step 4: Clean up artifacts (BEFORE git setup)
            self.logger.info("🧹 PHASE START: Cleaning up template artifacts...")
            self.logger.info("🎯 CRITICAL: Removing template directory BEFORE git commit...")
            
            if not self.project_cleaner.cleanup_project(target_dir):
                self.logger.error("❌ Cleanup failed! This will cause template artifacts to be committed.")
                return False
            else:
                self.logger.info("✅ PHASE END: Cleanup completed successfully.")

            # Step 5: Setup GitHub repository (AFTER cleanup)
            if project_config.get('create_github_repo', False):
                self.logger.info("🐙 PHASE START: Setting up GitHub repository...")
                self.logger.info("🎯 SAFE: Creating repository with CLEAN project (no template artifacts)")
                
                repo_url = self.github_manager.create_repository(
                    project_name=project_config['project_name'],
                    description=project_config['project_description'],
                    project_dir=target_dir,
                    org=project_config.get('github_org', 'SynaptixLabs'),
                    private=project_config.get('github_private', False),
                    auto_commit=True
                )
                if repo_url:
                    project_config['github_url'] = repo_url
                    self.logger.info(f"✅ PHASE END: GitHub repository setup completed: {repo_url}")
                else:
                    self.logger.warning("⚠️ PHASE END: GitHub repository setup failed.")
            else:
                self.logger.debug("⏭️ GitHub repository creation skipped.")
            
            # --- END OF CRITICAL FIX ---

            # Step 6: Validate project structure (confirms cleanup worked)
            self.logger.info("🔍 PHASE START: Validating project structure...")
            self.logger.info("🎯 VERIFICATION: Ensuring template directory was removed...")
            
            self._validate_project_with_report(target_dir)
            self.logger.info("✅ PHASE END: Project validation completed.")

            # Step 7: Generate TODO lists
            self.logger.info("📋 PHASE START: Generating TODO lists...")
            self._generate_todo_lists(target_dir, project_config)
            self.logger.info("✅ PHASE END: TODO lists generated.")

            # Step 8: Final success summary
            self._display_success_summary(project_config)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Project generation failed with a critical error: {e}")
            import traceback
            self.logger.debug(f"Full error traceback:\n{traceback.format_exc()}")
            return False

    def _get_project_configuration(self, template, interactive, target_dir, **kwargs) -> Optional[Dict[str, Any]]:
        available_templates = self.template_renderer.get_available_templates()
        if template is None and interactive:
            template = self._display_template_menu(available_templates)
        elif template is None:
            self.logger.error("Template must be specified in non-interactive mode")
            return None
        
        if template not in available_templates:
            self.logger.error(f"Template '{template}' not found")
            return None
        
        if interactive:
            project_data = self._get_interactive_project_data(target_dir)
            github_config = self._get_github_preferences()
        else:
            project_data = self._get_default_project_data(target_dir)
            github_config = {'create_github_repo': True}

        return {'template': template, 'template_info': available_templates[template], 'target_dir': target_dir, 'interactive': interactive, **project_data, **github_config, **kwargs}

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
                
    def _get_interactive_project_data(self, target_dir: Path) -> Dict[str, Any]:
        print("\n📝 Project Information")
        project_name = input(f"Project name [{target_dir.name}]: ").strip() or target_dir.name
        project_description = input("Project description: ").strip() or f"A project named {project_name}"
        author_name = input("Author name [Avidor]: ").strip() or "Avidor"
        author_email = input("Author email [avidor@synaptixlabs.ai]: ").strip() or "avidor@synaptixlabs.ai"
        return {'project_name': project_name, 'project_description': project_description, 'author_name': author_name, 'author_email': author_email, 'python_version': '3.12'}
    
    def _get_default_project_data(self, target_dir: Path) -> Dict[str, Any]:
        return {'project_name': target_dir.name, 'project_description': f"A new project: {target_dir.name}", 'author_name': 'Avidor', 'author_email': 'avidor@synaptixlabs.ai', 'python_version': '3.12'}

    def _get_github_preferences(self) -> Dict[str, Any]:
        print("\n🐙 GitHub Repository Setup")
        create_repo = input("Create GitHub repository? (Y/n): ").strip().lower() != 'n'
        if not create_repo:
            return {'create_github_repo': False}
        private = input("Make repository private? (Y/n): ").strip().lower() != 'n'
        org = input("GitHub organization [SynaptixLabs]: ").strip() or "SynaptixLabs"
        return {'create_github_repo': True, 'github_private': private, 'github_org': org}

    def _generate_todo_lists(self, target_dir: Path, config: Dict[str, Any]) -> None:
        try:
            template_type = config['template'].replace('python-', '')
            for sprint in range(1, 5):
                self.todo_generator.generate_todo_file(project_name=config['project_name'], template_type=template_type, sprint_number=sprint, output_dir=target_dir / 'docs')
        except Exception as e:
            self.logger.warning(f"TODO generation failed: {e}")
    
    def _validate_project_with_report(self, target_dir: Path) -> None:
        """
        Enhanced validation that specifically checks for template cleanup success.
        """
        try:
            logs_dir = target_dir / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            # Specific check for template directory (should NOT exist)
            template_dir = target_dir / "template"
            if template_dir.exists():
                self.logger.error(f"❌ CRITICAL: Template directory still exists at {template_dir}")
                self.logger.error("❌ This indicates cleanup failed and template artifacts were committed!")
                
                # Try emergency cleanup
                self.logger.warning("🚨 Attempting emergency cleanup...")
                if self.project_cleaner.cleanup_project(target_dir):
                    self.logger.info("✅ Emergency cleanup successful")
                else:
                    self.logger.error("❌ Emergency cleanup also failed")
            else:
                self.logger.info("✅ Template directory successfully removed")
            
            # Run full validation
            validation_success = self.project_validator.validate_project(target_dir)
            if not validation_success:
                self.logger.warning("⚠️ Project validation found issues.")
            else:
                self.logger.info("✅ Project validation passed all checks")
            
            # Move validation report
            validation_report_src = target_dir / "validation_report.md"
            if validation_report_src.exists():
                validation_report_dest = logs_dir / "validation_report.md"
                validation_report_src.rename(validation_report_dest)
                self.logger.info(f"📋 Validation report moved to: {validation_report_dest}")
                
        except Exception as e:
            self.logger.warning(f"Validation failed: {e}")

    def _display_success_summary(self, config: Dict[str, Any]) -> None:
        github_info = f"\n🐙 GitHub: {config['github_url']}" if config.get('github_url') else "\n🐙 GitHub: Not created."
        summary = f"""
🎉 Project '{config['project_name']}' Generated Successfully!

   Template: {config['template']}
   Location: {config['target_dir']}{github_info}

🎯 Next Steps:
   1. `cd {config['target_dir']}`
   2. `poetry install`
   3. `poetry run pre-commit install`
   4. `poetry run test`
   5. Start developing in the `src/` directory!

Happy coding! 🚀
"""
        print(summary)
        self.logger.info("🎆 WINDSURF PROJECT GENERATOR SESSION COMPLETED")

def main():
    parser = argparse.ArgumentParser(description="Windsurf Python Project Generator v5.4")
    parser.add_argument("--template", help="Template type to use")
    parser.add_argument("--non-interactive", action="store_true", help="Run with minimal prompts")
    parser.add_argument("--project-dir", type=Path, help="Target directory for project generation")
    args = parser.parse_args()
    
    generator = WindsurfGenerator()
    success = generator.generate_project(
        template=args.template,
        interactive=not args.non_interactive,
        project_dir=args.project_dir
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()