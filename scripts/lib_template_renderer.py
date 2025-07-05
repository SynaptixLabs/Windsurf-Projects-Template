#!/usr/bin/env python3
"""
Template Renderer Library

Handles core template rendering logic using Copier for the Windsurf project generator.
"""

import logging
import traceback
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

import copier
from rich.console import Console

# Try to import copier, but don't fail if it's not there yet.
# The _check_copier_available method will handle the user-facing error.
try:
    import copier
    import yaml
except ImportError:
    copier = None
    yaml = None

class TemplateRenderer:
    """Handles template rendering operations."""

    def __init__(self):
        self.logger = logging.getLogger('windsurf_generator')
        self.template_root = Path(__file__).parent.parent / "template-generators"

    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available templates."""
        return {
            "python-modern": {
                "description": "Generic modern Python project (supports all project types)",
                "is_base": True,
                "extends": None
            },
            "python-game-development": {
                "description": "Game development with Pygame (extends python-modern)",
                "is_base": False,
                "extends": "python-modern"
            },
            "python-agentic-ai": {
                "description": "CrewAI multi-agent systems (extends python-modern)",
                "is_base": False,
                "extends": "python-modern"
            },
            "python-data-science": {
                "description": "Data science with Polars and Prefect (extends python-modern)",
                "is_base": False,
                "extends": "python-modern"
            }
        }

    def render_project(self, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Render a complete project, handling base and overlay templates correctly.
        Returns the dictionary of final answers on success, None on failure.
        """
        try:
            template_name = config['template']
            template_info = config['template_info']
            target_dir = Path(config['target_dir'])

            self.logger.info(f"🚀 Rendering project: {config.get('project_name', 'new-project')}")

            if not self._check_copier_available():
                return None

            data_for_copier = self._prepare_template_data(config)
            final_results = None

            if template_info.get("is_base", False):
                final_results = self._run_copier(template_name, target_dir, data_for_copier)
            else:
                base_template = template_info.get("extends")
                if not base_template:
                    self.logger.error(f"Overlay template '{template_name}' does not specify which template it extends.")
                    return None
                
                base_results = self._run_copier(base_template, target_dir, data_for_copier)
                if not base_results:
                    self.logger.error(f"Failed to render base template '{base_template}'.")
                    return None
                
                answers = self._load_copier_answers(base_results.answers_file)
                if not answers:
                    self.logger.error("Could not load answers from base template. Cannot apply overlay.")
                    return None
                
                final_results = self._run_copier(template_name, target_dir, answers, overwrite=True)

            if final_results:
                answers = None
                # First, try to get answers directly from the results object, which is more reliable.
                if final_results.answers:
                    self.logger.info("✅ Copier returned answers directly in the result object.")
                    # The diagnostic logs revealed the .combined attribute holds the final answers.
                    answers = final_results.answers.combined
                # If not, fall back to loading from the answers file path if it exists.
                elif final_results.answers_file:
                    self.logger.info(f"✅ Loading answers from file: {final_results.answers_file}")
                    answers = self._load_copier_answers(final_results.answers_file)

                if answers:
                    self.logger.info("✅ Final answers successfully retrieved from copier.")
                    project_name = answers.get('project_name', config.get('project_name', "unknown-project"))
                    self._create_project_logs_directory(target_dir, project_name)
                    self._save_copier_answers(target_dir, answers)
                    return answers
                else:
                    self.logger.error("❌ Could not retrieve final answers from copier. Template rendering failed.")
                    return None
            else:
                self.logger.error("Template rendering failed because the final copier run was unsuccessful.")
                return None

        except Exception as e:
            self.logger.error(f"❌ Top-level template rendering failed: {e}")
            self.logger.debug(traceback.format_exc())
            return None

    def _load_copier_answers(self, answers_file: Path) -> Optional[Dict[str, Any]]:
        """Load the answers from the specified .copier-answers.yml file path."""
        if not answers_file or not answers_file.exists():
            self.logger.error(f"Copier answers file not found at the specified path: {answers_file}")
            return None
        try:
            self.logger.debug(f"Loading answers from {answers_file}...")
            with answers_file.open("r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading copier answers file '{answers_file}': {e}")
            return None

    def _prepare_template_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare template data for non-interactive runs."""
        project_slug = config['project_name'].lower().replace(' ', '-').replace('_', '-')
        data = {
            'project_name': config['project_name'],
            'project_description': config['project_description'],
            'author_name': config['author_name'],
            'author_email': config['author_email'],
            'python_version': config.get('python_version', '3.12'),
            'project_slug': project_slug,
        }

        # Pass through the complexity setting if it exists for non-interactive runs
        if 'complexity_preset' in config:
            data['complexity_preset'] = config['complexity_preset']
        
        if 'integration_focus' in config:
            data['integration_focus'] = config['integration_focus']

        return data

    def _check_copier_available(self) -> bool:
        """Check if Copier and PyYAML are available."""
        if copier and yaml:
            return True
        self.logger.error("❌ Error: Copier or PyYAML not installed")
        self.logger.error("Install with: pip install copier 'pyyaml>=5.4.1'")
        return False

    def _run_copier(self, template_name: str, target_dir: Path, data: Dict[str, Any], overwrite: bool = False) -> Optional['copier.main.Results']:
        """
        A single, robust method to run copier.
        Returns the Results object on success, None on failure.
        """
        template_path = self.template_root / template_name
        if not template_path.exists():
            self.logger.error(f"Template not found: {template_path}")
            return None
        try:


            self.logger.info(f"Running copier for '{template_name}'...")
            results = copier.run_copy(
                src_path=str(template_path),
                dst_path=str(target_dir),
                data=data,
                unsafe=True,
                overwrite=overwrite,
                cleanup_on_error=False  # Disable cleanup to debug copier failures
            )
            return results
        except Exception as e:
            self.logger.error(f"❌ Error running copier for template '{template_name}': {e}")
            self.logger.debug(traceback.format_exc())
            return None

    def _create_project_logs_directory(self, target_dir: Path, project_name: str) -> None:
        """Create logs directory structure in the generated project."""
        try:
            logs_dir = target_dir / "logs"
            logs_dir.mkdir(exist_ok=True)

            # Create .gitkeep to ensure the directory is tracked by git
            (logs_dir / ".gitkeep").touch()

            # Create a README for the logs directory
            readme_content = f"""# Logs for {project_name}

This directory is intended for application logs. It is included in `.gitignore` so that log files are not committed to the repository.

A `.gitkeep` file is included to ensure this empty directory is tracked by Git.
"""
            (logs_dir / "README.md").write_text(readme_content)

            self.logger.info(f"📁 Created logs directory for '{project_name}'")
        except Exception as e:
            self.logger.warning(f"Could not create logs directory for '{project_name}': {e}")

    def _sanitize_for_yaml(self, data: Any) -> Any:
        """Recursively sanitizes data to ensure it's YAML-safe."""
        if isinstance(data, dict):
            return {key: self._sanitize_for_yaml(value) for key, value in data.items()}
        if isinstance(data, list):
            return [self._sanitize_for_yaml(item) for item in data]
        # Allow basic, YAML-native types
        if isinstance(data, (str, int, float, bool, type(None))):
            return data
        # Convert all other types to their string representation
        return str(data)

    def _save_copier_answers(self, target_dir: Path, answers: Dict[str, Any]) -> None:
        """Saves the final answers to a .copier-answers.yml file in the project root."""
        answers_file_path = target_dir / ".copier-answers.yml"
        try:
            self.logger.info(f"📝 Saving final answers to {answers_file_path}...")
            with answers_file_path.open("w", encoding="utf-8") as f:
                # Filter out private copier keys (like _src_path) before saving
                filtered_answers = {k: v for k, v in answers.items() if not k.startswith('_')}
                # Sanitize the data to remove any complex Python objects before dumping
                sanitized_answers = self._sanitize_for_yaml(filtered_answers)
                yaml.dump(sanitized_answers, f, default_flow_style=False, sort_keys=False)
            self.logger.info("✅ Final answers saved successfully.")
        except Exception as e:
            self.logger.error(f"❌ Failed to save .copier-answers.yml file: {e}")
            self.logger.debug(traceback.format_exc())
