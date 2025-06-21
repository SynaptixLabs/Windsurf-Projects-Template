#!/usr/bin/env python3
"""
Windsurf Python Project Generator - Main Orchestrator

This is the main entry point for the Windsurf project template system.
It orchestrates all other library modules to provide a clean, maintainable
project generation workflow.

Version: 4.0 (Refactored Architecture)
"""

import sys
import argparse
import logging
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
        self.template_renderer = TemplateRenderer()
        self.github_manager = GitHubManager()
        self.project_cleaner = ProjectCleaner()
        self.project_validator = ProjectValidator()
        self.todo_generator = TODOGenerator()
        self.dependency_checker = DependencyChecker()
        
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the main generator."""
        logger = logging.getLogger('windsurf_generator')
        logger.setLevel(logging.DEBUG)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def generate_project(
        self,
        template: Optional[str] = None,
        interactive: bool = True,
        project_dir: Optional[Path] = None,
        **kwargs
    ) -> bool:
        """
        Main project generation workflow.
        
        Args:
            template: Template type to use
            interactive: Whether to run interactive mode
            project_dir: Target directory (defaults to current)
            **kwargs: Additional template data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Step 1: Pre-flight checks
            self.logger.info("🚀 Starting Windsurf project generation")
            
            if not self.dependency_checker.check_all_dependencies():
                self.logger.error("❌ Dependency check failed")
                return False
            
            # Step 2: Get project configuration
            project_config = self._get_project_configuration(
                template, interactive, project_dir, **kwargs
            )
            
            if not project_config:
                self.logger.error("❌ Failed to get project configuration")
                return False
            
            # Step 3: Render templates
            self.logger.info("📦 Rendering project templates...")
            if not self.template_renderer.render_project(project_config):
                self.logger.error("❌ Template rendering failed")
                return False
            
            # Step 4: Clean up artifacts
            self.logger.info("🧹 Cleaning up template artifacts...")
            if not self.project_cleaner.cleanup_project(project_config['target_dir']):
                self.logger.warning("⚠️ Cleanup had issues, but continuing...")
            
            # Step 5: Validate project structure
            self.logger.info("🔍 Validating project structure...")
            if not self.project_validator.validate_project(project_config['target_dir']):
                self.logger.warning("⚠️ Project validation found issues")
            
            # Step 6: Generate TODO lists
            self.logger.info("📋 Generating TODO lists...")
            self._generate_todo_lists(project_config)
            
            # Step 7: Setup GitHub repository (if requested)
            if project_config.get('create_github_repo', False):
                self.logger.info("🐙 Setting up GitHub repository...")
                repo_url = self.github_manager.create_repository(
                    project_config['project_name'],
                    project_config['project_description'],
                    project_config['target_dir'],
                    org=project_config.get('github_org', 'SynaptixLabs'),
                    private=project_config.get('github_private', False)
                )
                
                if repo_url:
                    self.logger.info(f"✅ GitHub repository created: {repo_url}")
                    project_config['github_url'] = repo_url
                else:
                    self.logger.warning("⚠️ GitHub repository creation failed")
            
            # Step 8: Final validation
            self.logger.info("✅ Final project validation...")
            if not self.project_validator.validate_project(project_config['target_dir']):
                self.logger.warning("⚠️ Final validation found issues")
            
            # Step 9: Success summary
            self._display_success_summary(project_config)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Project generation failed: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False
    
    def _get_project_configuration(
        self,
        template: Optional[str],
        interactive: bool,
        project_dir: Optional[Path],
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """Get complete project configuration."""
        try:
            # Get available templates
            available_templates = self.template_renderer.get_available_templates()
            
            # Select template
            if template is None and interactive:
                template = self._display_template_menu(available_templates)
            elif template is None:
                self.logger.error("Template must be specified in non-interactive mode")
                return None
            
            if template not in available_templates:
                self.logger.error(f"Template '{template}' not found")
                return None
            
            # Get target directory
            target_dir = project_dir or Path.cwd()
            
            # Get project data
            if interactive:
                project_data = self._get_interactive_project_data()
            else:
                project_data = self._get_default_project_data()
            
            # Get GitHub preferences
            github_config = {}
            if interactive:
                github_config = self._get_github_preferences()
            
            # Combine all configuration
            config = {
                'template': template,
                'template_info': available_templates[template],
                'target_dir': target_dir,
                'interactive': interactive,
                **project_data,
                **github_config,
                **kwargs
            }
            
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to get project configuration: {e}")
            return None
    
    def _display_template_menu(self, templates: Dict[str, Any]) -> Optional[str]:
        """Display interactive template selection menu."""
        print("\n🎯 Windsurf Python Project Generator v4.0")
        print("=" * 50)
        print("Select a template to generate your project:\n")
        
        template_list = list(templates.items())
        
        for i, (template_name, template_info) in enumerate(template_list, 1):
            inheritance_info = ""
            if template_info.get("extends"):
                inheritance_info = f" (extends {template_info['extends']})"
            
            print(f"{i}. {template_name}")
            print(f"   {template_info['description']}{inheritance_info}")
            if 'details' in template_info:
                print(f"   Details: {template_info['details']}")
            print()
        
        while True:
            try:
                choice = input(f"Enter your choice (1-{len(template_list)}): ").strip()
                
                if choice.lower() in ['q', 'quit', 'exit']:
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(template_list):
                    selected_template = template_list[choice_num - 1][0]
                    
                    print(f"\n✅ Selected: {selected_template}")
                    confirm = input(f"Proceed with {selected_template}? (y/N): ").strip().lower()
                    if confirm in ['y', 'yes']:
                        return selected_template
                    else:
                        print("\n🔄 Let's try again...\n")
                        continue
                else:
                    print(f"❌ Please enter a number between 1 and {len(template_list)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                return None
    
    def _get_interactive_project_data(self) -> Dict[str, Any]:
        """Get project data interactively."""
        print("\n📝 Project Information")
        print("-" * 30)
        
        current_dir = Path.cwd()
        default_name = current_dir.name
        
        project_name = input(f"Project name [{default_name}]: ").strip()
        if not project_name:
            project_name = default_name
        
        project_description = input("Project description: ").strip()
        if not project_description:
            project_description = f"A Python project built with modern tooling"
        
        author_name = input("Author name [Avidor]: ").strip()
        if not author_name:
            author_name = "Avidor"
        
        author_email = input("Author email [avidor@synaptixlabs.ai]: ").strip()
        if not author_email:
            author_email = "avidor@synaptixlabs.ai"
        
        return {
            'project_name': project_name,
            'project_description': project_description,
            'author_name': author_name,
            'author_email': author_email,
            'python_version': '3.12'
        }
    
    def _get_default_project_data(self) -> Dict[str, Any]:
        """Get default project data for non-interactive mode."""
        current_dir = Path.cwd()
        
        return {
            'project_name': current_dir.name,
            'project_description': 'A Python project built with modern tooling',
            'author_name': 'Avidor',
            'author_email': 'avidor@synaptixlabs.ai',
            'python_version': '3.12'
        }
    
    def _get_github_preferences(self) -> Dict[str, Any]:
        """Get GitHub repository preferences."""
        print("\n🐙 GitHub Repository Setup")
        print("-" * 30)
        
        create_repo = input("Create GitHub repository? (y/N): ").strip().lower()
        if create_repo not in ['y', 'yes']:
            return {'create_github_repo': False}
        
        private = input("Make repository private? (y/N): ").strip().lower()
        is_private = private in ['y', 'yes']
        
        org = input("GitHub organization [SynaptixLabs]: ").strip()
        if not org:
            org = "SynaptixLabs"
        
        return {
            'create_github_repo': True,
            'github_private': is_private,
            'github_org': org
        }
    
    def _generate_todo_lists(self, config: Dict[str, Any]) -> None:
        """Generate TODO lists for the project."""
        try:
            template_type = self._map_template_to_todo_type(config['template'])
            
            # Generate TODO lists for multiple sprints
            for sprint in range(1, 5):  # Generate 4 sprints
                todo_file = self.todo_generator.generate_todo_file(
                    project_name=config['project_name'],
                    template_type=template_type,
                    sprint_number=sprint,
                    output_dir=config['target_dir'] / 'docs'
                )
                
                if todo_file:
                    self.logger.debug(f"Generated TODO file: {todo_file}")
        
        except Exception as e:
            self.logger.warning(f"TODO generation failed: {e}")
    
    def _map_template_to_todo_type(self, template: str) -> str:
        """Map template name to TODO template type."""
        mapping = {
            'python-game-development': 'game-development',
            'python-agentic-ai': 'agentic-ai',
            'python-data-science': 'data-science',
            'python-modern': 'web-api'
        }
        return mapping.get(template, 'custom-multi')
    
    def _display_success_summary(self, config: Dict[str, Any]) -> None:
        """Display project generation success summary."""
        github_info = ""
        if config.get('github_url'):
            github_info = f"\n🐙 GitHub: {config['github_url']}"
        
        project_slug = config['project_name'].lower().replace(' ', '-').replace('_', '-')
        
        print(f"""
🎉 Project Generated Successfully!

📊 Generation Summary:
   📁 Project: {config['project_name']}
   📋 Template: {config['template']}
   🐍 Python: {config.get('python_version', '3.12')}
   👤 Author: {config['author_name']} <{config['author_email']}>{github_info}

✨ Features Applied:
   🧹 Automatic template artifact cleanup
   🐙 GitHub repository integration
   🔍 Project structure validation
   📋 Sprint-based TODO generation

🎯 Next Steps:

1. Install dependencies:
   poetry install

2. Setup development environment:
   poetry run pre-commit install

3. Test the setup:
   poetry run ci      # Run full CI pipeline
   poetry run test    # Run tests
   poetry run lint    # Run linting

4. Review project structure:
   📁 src/{project_slug.replace('-', '_')}/  # Main source code
   📁 tests/                                 # Test suite  
   📁 docs/                                  # Documentation & TODO lists
   📁 logs/                                  # Application logs

5. Start development:
   poetry run dev     # Development mode

Happy coding! 🚀
""")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Windsurf Python Project Generator v4.0 - Refactored Architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
✨ Version 4.0 Features:
  • Modular library-based architecture
  • Automatic cleanup of template artifacts
  • Robust GitHub repository creation with fallbacks
  • Comprehensive project validation
  • Sprint-based TODO generation
  • Enhanced error handling and logging

Interactive Mode (Default):
  python windsurf_generator.py
  
Non-Interactive Mode:
  python windsurf_generator.py --template python-game-development --non-interactive
  
List Templates:
  python windsurf_generator.py --list-templates
"""
    )
    
    parser.add_argument("--template", 
                       help="Template type to use (skips interactive menu)")
    
    parser.add_argument("--non-interactive", 
                       action="store_true",
                       help="Run with minimal prompts (requires --template)")
    
    parser.add_argument("--list-templates",
                       action="store_true", 
                       help="List available templates and exit")
    
    parser.add_argument("--project-dir",
                       type=Path,
                       help="Target directory for project generation")
    
    args = parser.parse_args()
    
    # Create generator instance
    generator = WindsurfGenerator()
    
    if args.list_templates:
        templates = generator.template_renderer.get_available_templates()
        print("📋 Available Templates:")
        for name, info in templates.items():
            inheritance = f" (extends {info.get('extends', 'none')})" if info.get('extends') else ""
            print(f"  • {name}: {info['description']}{inheritance}")
            if 'details' in info:
                print(f"    Details: {info['details']}")
        return
    
    if args.non_interactive and not args.template:
        print("❌ Error: --non-interactive requires --template")
        parser.print_help()
        sys.exit(1)
    
    try:
        success = generator.generate_project(
            template=args.template,
            interactive=not args.non_interactive,
            project_dir=args.project_dir
        )
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
