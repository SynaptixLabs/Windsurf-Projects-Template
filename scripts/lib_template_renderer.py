#!/usr/bin/env python3
"""
Template Renderer Library

Handles core template rendering logic using Copier for the Windsurf project generator.
Extracted from windsurf_generate.py for better modularity.
"""

import os
import shutil
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
import datetime


class TemplateRenderer:
    """Handles template rendering operations."""
    
    def __init__(self):
        self.logger = logging.getLogger('template_renderer')
        self.template_root = Path(__file__).parent.parent / "template-generators"
    
    def get_available_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available templates."""
        return {
            "python-modern": {
                "description": "Generic modern Python project (supports all project types)",
                "is_base": True,
                "extends": None,
                "details": "Web API, Agentic AI, Data Science, CLI Tools, Libraries"
            },
            "python-game-development": {
                "description": "Game development with Pygame (extends python-modern)",
                "is_base": False,
                "extends": "python-modern",
                "details": "Modern Python + Pygame, performance profiling, game-specific tools"
            },
            "python-agentic-ai": {
                "description": "CrewAI multi-agent systems (extends python-modern)",
                "is_base": False,
                "extends": "python-modern",
                "details": "Modern Python + CrewAI, vector databases, agent orchestration"
            },
            "python-data-science": {
                "description": "Data science with Polars and Prefect (extends python-modern)",
                "is_base": False,
                "extends": "python-modern",
                "details": "Modern Python + Polars, DuckDB, Prefect, Jupyter integration"
            }
        }
    
    def render_project(self, config: Dict[str, Any]) -> bool:
        """
        Render a complete project using template inheritance.
        
        Args:
            config: Project configuration containing template info and data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Setup detailed logging for this generation
            project_logger = self._setup_project_logging(config)
            
            # Prepare template data
            template_data = self._prepare_template_data(config)
            
            # Get template information
            template = config['template']
            template_info = config['template_info']
            target_dir = config['target_dir']
            
            project_logger.info(f"🚀 Rendering project: {config['project_name']}")
            project_logger.info(f"📁 Target directory: {target_dir}")
            project_logger.info(f"📋 Template: {template} ({template_info['description']})")
            
            # Check for copier dependency
            if not self._check_copier_available():
                return False
            
            if template_info["is_base"]:
                # Simple case: Use base template only
                project_logger.info("📦 Using base template (no inheritance)")
                success = self._render_base_template(template, target_dir, template_data)
                
            else:
                # Complex case: Template inheritance
                base_template = template_info["extends"]
                project_logger.info(f"🔗 Using template inheritance: {base_template} → {template}")
                
                # Configure template data for specific project types
                template_data = self._configure_template_data_for_type(template, template_data)
                
                # Step 1: Generate base template
                success = self._render_base_template(base_template, target_dir, template_data)
                if not success:
                    project_logger.error("❌ Base template generation failed")
                    return False
                
                # Step 2: Apply overlay template
                success = self._apply_template_overlay(template, target_dir, template_data)
                if not success:
                    project_logger.error("❌ Template overlay application failed")
                    return False
            
            if success:
                # Create project logs directory
                self._create_project_logs_directory(target_dir, config['project_name'])
                project_logger.info("✅ Template rendering completed successfully")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Template rendering failed: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False
    
    def _setup_project_logging(self, config: Dict[str, Any]) -> logging.Logger:
        """Setup comprehensive logging for project generation."""
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Setup project-specific logger
        project_name = config['project_name']
        logger = logging.getLogger(f'template_renderer.{project_name}')
        logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # File handler for detailed logs
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = logs_dir / f"generation_{project_name}_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler for user feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        file_handler.setFormatter(detailed_formatter)
        console_handler.setFormatter(simple_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        logger.info(f"🚀 Starting template rendering for: {project_name}")
        logger.info(f"📝 Detailed logs will be saved to: {log_file}")
        
        return logger
    
    def _prepare_template_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare comprehensive template data."""
        # Start with defaults
        template_data = self._get_default_template_data()
        
        # Update with config data
        template_data.update({
            'project_name': config['project_name'],
            'project_description': config['project_description'],
            'author_name': config['author_name'],
            'author_email': config['author_email'],
            'python_version': config.get('python_version', '3.12')
        })
        
        # Generate project slug
        project_slug = config['project_name'].lower().replace(' ', '-').replace('_', '-')
        if project_slug and project_slug[0].isdigit():
            digit_map = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', 
                        '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '0': 'zero'}
            if project_slug[0] in digit_map:
                project_slug = digit_map[project_slug[0]] + project_slug[1:]
        
        template_data['project_slug'] = project_slug
        template_data['game_title'] = config['project_name']  # For game projects
        
        return template_data
    
    def _get_default_template_data(self) -> Dict[str, Any]:
        """Get comprehensive default template data."""
        return {
            # Basic project info
            "project_name": "",
            "project_slug": "",
            "project_description": "",
            "author_name": "Avidor",
            "author_email": "avidor@synaptixlabs.ai",
            "python_version": "3.12",
            
            # Project type and features
            "project_type": "library",
            "package_manager": "poetry",
            "databases": [],
            "testing_framework": "comprehensive",
            "coverage_threshold": 85,
            
            # Feature flags
            "include_docker": True,
            "include_github_actions": True,
            "include_pre_commit": True,
            "include_docs": True,
            "include_windsurf": True,
            "include_auth": False,
            "include_notebooks": False,
            "include_assets": False,
            
            # API settings
            "api_version": "v1",
            
            # CrewAI settings
            "crewai_features": ["basic-agents", "tools"],
            
            # Data science settings
            "orchestration_tool": "prefect",
            
            # Game development settings
            "game_type": "2d-arcade",
            "game_framework": "pygame",
            "target_fps": 60,
            
            # Sprint/TODO settings
            "use_sprint_based_todos": True,
            "sprint_duration_weeks": 2,
            "total_sprints": 4,
            
            # Advanced settings
            "include_performance_profiling": False,
            "testing_level": "comprehensive",
            "documentation_level": "standard",
            "include_cicd": True,
            "include_logging": True,
            "include_config_management": True,
            
            # Common template variables
            "env": os.environ.copy(),
            "year": "2025",
            "license": "MIT",
            
            # Game-specific defaults
            "has_project_spec": False,
            "game_category": "board_game",
            "project_spec_source": "will_create_interactively",
            
            # Author/GitHub settings
            "author_github_url": "https://github.com/SynaptixLabs",
            
            # Additional common variables
            "version": "0.1.0",
            "game_title": "",
            "board_size": "7x6",
            
            # GitHub Actions context (simplified)
            "github": {},
            "runner": {},
        }
    
    def _configure_template_data_for_type(self, template: str, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Configure template data for specific project types."""
        if template == "python-game-development":
            template_data.update({
                "project_type": "game-development",
                "include_performance_profiling": True,
                "testing_framework": "comprehensive"
            })
            self.logger.debug("🎮 Configured for game development")
            
        elif template == "python-agentic-ai":
            template_data.update({
                "project_type": "agentic-ai",
                "databases": ["chromadb"]
            })
            self.logger.debug("🤖 Configured for agentic AI")
            
        elif template == "python-data-science":
            template_data.update({
                "project_type": "data-science",
                "databases": ["duckdb"],
                "orchestration_tool": "prefect"
            })
            self.logger.debug("📊 Configured for data science")
        
        return template_data
    
    def _check_copier_available(self) -> bool:
        """Check if Copier is available."""
        try:
            import copier
            self.logger.debug("✅ Copier import successful")
            return True
        except ImportError:
            self.logger.error("❌ Error: Copier not installed")
            self.logger.error("Install with: pip install copier")
            return False
    
    def _render_base_template(
        self,
        base_template: str,
        target_dir: Path,
        template_data: Dict[str, Any]
    ) -> bool:
        """Render the base template."""
        base_template_path = self.template_root / base_template
        
        if not base_template_path.exists():
            self.logger.error(f"Base template not found: {base_template_path}")
            return False
        
        try:
            import copier
            
            self.logger.info(f"📦 Generating base template: {base_template}")
            
            result = copier.run_copy(
                str(base_template_path),
                str(target_dir),
                data=template_data,
                unsafe=True,
                vcs_ref=None,
                skip_tasks=True,  # Skip post-generation tasks
                overwrite=True    # Allow overwriting files
            )
            
            self.logger.info(f"✅ Base template '{base_template}' generated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error generating base template: {e}")
            self.logger.debug(f"Template path: {base_template_path}")
            self.logger.debug(f"Target directory: {target_dir}")
            
            import traceback
            self.logger.debug("Full error traceback:")
            self.logger.debug(traceback.format_exc())
            return False
    
    def _apply_template_overlay(
        self,
        overlay_template: str,
        target_dir: Path,
        template_data: Dict[str, Any]
    ) -> bool:
        """Apply template overlay files on top of base template."""
        overlay_template_path = self.template_root / overlay_template
        
        if not overlay_template_path.exists():
            self.logger.error(f"Overlay template not found: {overlay_template_path}")
            return False
        
        try:
            # Create temporary directory for overlay generation
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir) / "overlay"
                temp_path.mkdir()
                
                import copier
                
                self.logger.info(f"🎨 Applying template overlay: {overlay_template}")
                
                # Generate overlay template in temp directory
                result = copier.run_copy(
                    str(overlay_template_path),
                    str(temp_path),
                    data=template_data,
                    unsafe=True,
                    vcs_ref=None,
                    skip_tasks=True,  # Skip post-generation tasks
                    overwrite=True    # Allow overwriting files
                )
                
                # Copy overlay files to target, excluding problematic ones
                overlay_count = 0
                excluded_patterns = ['.DISABLE', '.jinja.bak', 'template_DELETE_ME']
                
                for item in temp_path.rglob("*"):
                    if item.is_file():
                        # Skip excluded patterns
                        if any(pattern in str(item) for pattern in excluded_patterns):
                            self.logger.debug(f"   ⏭️ Skipped: {item.relative_to(temp_path)}")
                            continue
                        
                        # Calculate relative path
                        rel_path = item.relative_to(temp_path)
                        target_file = target_dir / rel_path
                        
                        # Ensure parent directory exists
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Copy overlay file (this will overwrite base file if it exists)
                        shutil.copy2(item, target_file)
                        overlay_count += 1
                        self.logger.debug(f"   📄 {rel_path}")
            
            self.logger.info(f"✅ Applied {overlay_count} overlay files from '{overlay_template}'")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error applying template overlay: {e}")
            import traceback
            self.logger.debug(traceback.format_exc())
            return False
    
    def _create_project_logs_directory(self, target_dir: Path, project_name: str) -> None:
        """Create logs directory structure in the generated project."""
        try:
            logs_dir = target_dir / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            # Create .gitkeep to preserve directory
            gitkeep_file = logs_dir / ".gitkeep"
            gitkeep_file.write_text("# Keep this directory in git but ignore log files\n")
            
            # Create README for logs directory
            readme_content = f"""# Logs Directory

This directory contains application logs for {project_name}.

## Log Files

- `app.log` - Main application logs
- `debug.log` - Debug information  
- `error.log` - Error logs
- `performance.log` - Performance metrics
- `generation.log` - Project generation logs

## Log Rotation

Logs are automatically rotated when they exceed 10MB.
Old logs are kept for 30 days by default.

## Configuration

Log levels and destinations can be configured in:
- `src/{project_name.replace('-', '_')}/config/settings.py`
- Environment variables (LOG_LEVEL, LOG_FILE)
"""
            
            readme_file = logs_dir / "README.md"
            readme_file.write_text(readme_content)
            
            self.logger.info(f"📁 Created logs directory structure in {logs_dir}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create logs directory: {e}")
