#!/usr/bin/env python3
"""
Project Cleanup Library

Handles cleanup of template artifacts and post-generation cleaning.
Extracted from external_project_cleanup.py and enhanced_windsurf_generator_v3.py.
"""

import shutil
import logging
from pathlib import Path
from typing import List, Set, Optional, Dict
import os
import stat


class ProjectCleaner:
    """Handles cleanup of template artifacts from generated projects."""
    
    def __init__(self):
        self.logger = logging.getLogger('project_cleaner')
        
        # Define cleanup patterns
        self.artifact_patterns = [
            '*.DISABLE*',
            '*.jinja.bak*',
            '*DELETE_ME*',
            '*.template*',
            'copier-answers.yml',
            '.copier-answers.yml'
        ]
        
        # Directories to remove completely
        self.artifact_directories = [
            'template',
            'template_DELETE_ME',
            '__pycache__',
            '.pytest_cache'
        ]
        
        # Files to remove
        self.artifact_files = [
            '.copier-answers.yml',
            'copier-answers.yml'
        ]
    
    def cleanup_project(self, project_dir: Path) -> bool:
        """
        Clean up template artifacts from a generated project.
        
        Args:
            project_dir: Path to the generated project directory
            
        Returns:
            True if cleanup was successful, False otherwise
        """
        try:
            self.logger.info(f"🧹 Starting cleanup of project directory: {project_dir}")
            
            cleaned_items = []
            
            # Step 1: Remove template artifacts directories
            cleaned_items.extend(self._remove_artifact_directories(project_dir))
            
            # Step 2: Remove template artifact files
            cleaned_items.extend(self._remove_artifact_files(project_dir))
            
            # Step 3: Remove files matching patterns
            cleaned_items.extend(self._remove_pattern_files(project_dir))
            
            # Step 4: Clean up empty directories
            cleaned_items.extend(self._remove_empty_directories(project_dir))
            
            # Step 5: Fix file permissions if needed
            self._fix_file_permissions(project_dir)
            
            if cleaned_items:
                self.logger.info(f"🧹 Cleaned up {len(cleaned_items)} items: {', '.join(cleaned_items[:10])}")
                if len(cleaned_items) > 10:
                    self.logger.info(f"   ... and {len(cleaned_items) - 10} more items")
            else:
                self.logger.info("✅ No template artifacts found to clean")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Cleanup failed: {e}")
            return False
    
    def _remove_artifact_directories(self, project_dir: Path) -> List[str]:
        """Remove artifact directories."""
        cleaned = []
        
        for dir_name in self.artifact_directories:
            for artifact_dir in project_dir.rglob(dir_name):
                if artifact_dir.is_dir():
                    try:
                        shutil.rmtree(artifact_dir)
                        cleaned.append(f"{artifact_dir.relative_to(project_dir)}/")
                        self.logger.debug(f"   🗑️ Removed directory: {artifact_dir.relative_to(project_dir)}")
                    except Exception as e:
                        self.logger.warning(f"Failed to remove directory {artifact_dir}: {e}")
        
        return cleaned
    
    def _remove_artifact_files(self, project_dir: Path) -> List[str]:
        """Remove specific artifact files."""
        cleaned = []
        
        for file_name in self.artifact_files:
            for artifact_file in project_dir.rglob(file_name):
                if artifact_file.is_file():
                    try:
                        artifact_file.unlink()
                        cleaned.append(str(artifact_file.relative_to(project_dir)))
                        self.logger.debug(f"   🗑️ Removed file: {artifact_file.relative_to(project_dir)}")
                    except Exception as e:
                        self.logger.warning(f"Failed to remove file {artifact_file}: {e}")
        
        return cleaned
    
    def _remove_pattern_files(self, project_dir: Path) -> List[str]:
        """Remove files matching artifact patterns."""
        cleaned = []
        
        for pattern in self.artifact_patterns:
            for artifact_file in project_dir.rglob(pattern):
                if artifact_file.is_file():
                    try:
                        artifact_file.unlink()
                        cleaned.append(str(artifact_file.relative_to(project_dir)))
                        self.logger.debug(f"   🗑️ Removed pattern file: {artifact_file.relative_to(project_dir)}")
                    except Exception as e:
                        self.logger.warning(f"Failed to remove pattern file {artifact_file}: {e}")
        
        return cleaned
    
    def _remove_empty_directories(self, project_dir: Path) -> List[str]:
        """Remove empty directories (except protected ones)."""
        cleaned = []
        protected_dirs = {'.git', 'logs', '__pycache__', '.pytest_cache'}
        
        # Walk directories bottom-up to handle nested empty directories
        for dir_path in sorted(project_dir.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if (dir_path.is_dir() and 
                dir_path.name not in protected_dirs and
                not any(dir_path.iterdir()) and  # Directory is empty
                dir_path != project_dir):  # Don't remove the project root
                
                try:
                    dir_path.rmdir()
                    cleaned.append(f"{dir_path.relative_to(project_dir)}/")
                    self.logger.debug(f"   🗑️ Removed empty directory: {dir_path.relative_to(project_dir)}")
                except Exception as e:
                    self.logger.debug(f"Couldn't remove directory {dir_path}: {e}")
        
        return cleaned
    
    def _fix_file_permissions(self, project_dir: Path) -> None:
        """Fix file permissions if needed (mainly for Unix systems)."""
        try:
            for file_path in project_dir.rglob('*'):
                if file_path.is_file():
                    # Make sure files are readable
                    current_permissions = file_path.stat().st_mode
                    if not (current_permissions & stat.S_IRUSR):
                        file_path.chmod(current_permissions | stat.S_IRUSR)
                        self.logger.debug(f"   🔧 Fixed permissions: {file_path.relative_to(project_dir)}")
        except Exception as e:
            self.logger.debug(f"Permission fix failed: {e}")
    
    def get_cleanup_preview(self, project_dir: Path) -> Dict[str, List[str]]:
        """
        Get a preview of what would be cleaned without actually cleaning.
        
        Args:
            project_dir: Path to the project directory
            
        Returns:
            Dictionary with categories of items that would be cleaned
        """
        preview = {
            'directories': [],
            'files': [],
            'pattern_files': [],
            'empty_directories': []
        }
        
        # Preview directories to remove
        for dir_name in self.artifact_directories:
            for artifact_dir in project_dir.rglob(dir_name):
                if artifact_dir.is_dir():
                    preview['directories'].append(str(artifact_dir.relative_to(project_dir)))
        
        # Preview files to remove
        for file_name in self.artifact_files:
            for artifact_file in project_dir.rglob(file_name):
                if artifact_file.is_file():
                    preview['files'].append(str(artifact_file.relative_to(project_dir)))
        
        # Preview pattern files
        for pattern in self.artifact_patterns:
            for artifact_file in project_dir.rglob(pattern):
                if artifact_file.is_file():
                    preview['pattern_files'].append(str(artifact_file.relative_to(project_dir)))
        
        # Preview empty directories
        protected_dirs = {'.git', 'logs', '__pycache__', '.pytest_cache'}
        for dir_path in project_dir.rglob('*'):
            if (dir_path.is_dir() and 
                dir_path.name not in protected_dirs and
                not any(dir_path.iterdir()) and
                dir_path != project_dir):
                preview['empty_directories'].append(str(dir_path.relative_to(project_dir)))
        
        return preview
    
    def cleanup_logs_directory(self, project_dir: Path, keep_latest: int = 5) -> bool:
        """
        Clean up old log files, keeping only the most recent ones.
        
        Args:
            project_dir: Project directory
            keep_latest: Number of latest log files to keep
            
        Returns:
            True if successful
        """
        try:
            logs_dir = project_dir / 'logs'
            if not logs_dir.exists():
                return True
            
            # Get all log files sorted by modification time
            log_files = [f for f in logs_dir.glob('*.log') if f.is_file()]
            log_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Remove old log files
            files_to_remove = log_files[keep_latest:]
            removed_count = 0
            
            for log_file in files_to_remove:
                try:
                    log_file.unlink()
                    removed_count += 1
                    self.logger.debug(f"   🗑️ Removed old log: {log_file.name}")
                except Exception as e:
                    self.logger.warning(f"Failed to remove log file {log_file}: {e}")
            
            if removed_count > 0:
                self.logger.info(f"🧹 Cleaned up {removed_count} old log files")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Log cleanup failed: {e}")
            return False


if __name__ == "__main__":
    # Test functionality
    import argparse
    
    parser = argparse.ArgumentParser(description="Project Cleanup Test")
    parser.add_argument("project_dir", type=Path, help="Project directory to clean")
    parser.add_argument("--preview", action="store_true", help="Preview cleanup without executing")
    parser.add_argument("--logs-only", action="store_true", help="Clean only log files")
    
    args = parser.parse_args()
    
    cleaner = ProjectCleaner()
    
    if args.preview:
        preview = cleaner.get_cleanup_preview(args.project_dir)
        print("🔍 Cleanup Preview:")
        for category, items in preview.items():
            if items:
                print(f"   {category}: {len(items)} items")
                for item in items[:5]:  # Show first 5 items
                    print(f"     - {item}")
                if len(items) > 5:
                    print(f"     ... and {len(items) - 5} more")
    elif args.logs_only:
        success = cleaner.cleanup_logs_directory(args.project_dir)
        print(f"{'✅' if success else '❌'} Log cleanup {'completed' if success else 'failed'}")
    else:
        success = cleaner.cleanup_project(args.project_dir)
        print(f"{'✅' if success else '❌'} Project cleanup {'completed' if success else 'failed'}")
