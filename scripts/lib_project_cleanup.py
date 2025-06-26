#!/usr/bin/env python3
"""
Enhanced Project Cleanup Library
Removes template artifacts and development debris from generated projects.
Ensures clean project state before git operations.
"""

import shutil
import logging
from pathlib import Path
from typing import List, Tuple, Dict
import os
import glob


class ProjectCleaner:
    """Enhanced project cleaner with comprehensive artifact removal"""
    
    def __init__(self):
        self.logger = logging.getLogger('project_cleaner')
        
        # Directories to remove (template artifacts and dev debris)
        self.artifact_directories = [
            'template',           # Main template directory
            'template_DELETE_ME', # Backup naming convention
            'templates',          # Plural variant
            '.template',          # Hidden template dirs
            '__template__',       # Python-style naming
            '__pycache__',        # Python cache
            '.pytest_cache',      # Pytest cache
            '.mypy_cache',        # MyPy cache
            'node_modules',       # Node.js dependencies
            '.venv',              # Virtual environment (if accidentally included)
            'venv',               # Virtual environment
            '.env',               # Environment directory
            '.tox',               # Tox testing
            'htmlcov',            # Coverage reports
            '.coverage',          # Coverage data
            'dist',               # Distribution files
            'build',              # Build artifacts
            '*.egg-info',         # Python package info
        ]
        
        # Files to remove (template-related and temporary files)
        self.artifact_files = [
            'template.json',
            'template.yaml', 
            'template.yml',
            '.template_config',
            'generator_config.json',
            'template_metadata.json',
            '.env.local',
            '.env.development',
            '.env.test',
            '*.tmp',
            '*.temp',
            '*.bak',
            '*.orig',
            '.DS_Store',          # macOS system files
            'Thumbs.db',          # Windows system files
            'desktop.ini',        # Windows system files
            'copier-answers.yml',
            '.copier-answers.yml'
        ]
        
        # Patterns that should never be in generated projects
        self.forbidden_patterns = [
            '**/template/**',
            '**/templates/**',
            '**/.template/**',
            '**/generator_*',
            '**/template_*',
            '**/*.template',
            '*.DISABLE*',
            '*.jinja.bak*',
            '*DELETE_ME*'
        ]
    
    def cleanup_project(self, project_dir: Path) -> bool:
        """
        Enhanced cleanup with comprehensive logging and error handling
        
        Args:
            project_dir: Path to the generated project directory
            
        Returns:
            bool: True if cleanup successful, False if errors occurred
        """
        success = True
        cleanup_log = []
        project_path = Path(project_dir)
        
        if not project_path.exists():
            self.logger.error(f"Project directory does not exist: {project_dir}")
            return False
        
        self.logger.info(f"🧹 Starting cleanup of project: {project_dir}")
        
        # Phase 1: Clean artifact directories
        success &= self._clean_directories(project_path, cleanup_log)
        
        # Phase 2: Clean artifact files
        success &= self._clean_files(project_path, cleanup_log)
        
        # Phase 3: Clean by patterns (recursive)
        success &= self._clean_by_patterns(project_path, cleanup_log)
        
        # Phase 4: Clean empty directories
        success &= self._clean_empty_directories(project_path, cleanup_log)
        
        # Log cleanup summary
        if cleanup_log:
            self.logger.info("📋 Cleanup Summary:")
            for log_entry in cleanup_log:
                self.logger.info(f"  {log_entry}")
        else:
            self.logger.info("✨ No artifacts found - project was already clean")
        
        if success:
            self.logger.info("✅ Project cleanup completed successfully")
        else:
            self.logger.warning("⚠️ Project cleanup completed with some errors")
        
        return success
    
    def _clean_directories(self, project_path: Path, cleanup_log: List[str]) -> bool:
        """Clean artifact directories"""
        success = True
        
        for dir_name in self.artifact_directories:
            if dir_name.startswith('*'):
                # Handle glob patterns
                pattern_paths = list(project_path.glob(dir_name))
                for pattern_path in pattern_paths:
                    if pattern_path.is_dir():
                        success &= self._remove_directory(pattern_path, cleanup_log)
            else:
                # Handle direct directory names
                dir_path = project_path / dir_name
                if dir_path.exists() and dir_path.is_dir():
                    success &= self._remove_directory(dir_path, cleanup_log)
        
        return success
    
    def _clean_files(self, project_path: Path, cleanup_log: List[str]) -> bool:
        """Clean artifact files"""
        success = True
        
        for file_pattern in self.artifact_files:
            if '*' in file_pattern:
                # Handle glob patterns
                pattern_paths = list(project_path.glob(file_pattern))
                for pattern_path in pattern_paths:
                    if pattern_path.is_file():
                        success &= self._remove_file(pattern_path, cleanup_log)
            else:
                # Handle direct file names
                file_path = project_path / file_pattern
                if file_path.exists() and file_path.is_file():
                    success &= self._remove_file(file_path, cleanup_log)
        
        return success
    
    def _clean_by_patterns(self, project_path: Path, cleanup_log: List[str]) -> bool:
        """Clean using recursive patterns"""
        success = True
        
        for pattern in self.forbidden_patterns:
            try:
                pattern_paths = list(project_path.glob(pattern))
                for pattern_path in pattern_paths:
                    if pattern_path.is_dir():
                        success &= self._remove_directory(pattern_path, cleanup_log)
                    elif pattern_path.is_file():
                        success &= self._remove_file(pattern_path, cleanup_log)
            except Exception as e:
                self.logger.error(f"Error processing pattern {pattern}: {e}")
                success = False
        
        return success
    
    def _clean_empty_directories(self, project_path: Path, cleanup_log: List[str]) -> bool:
        """Remove empty directories that may have been left behind"""
        success = True
        removed_dirs = []
        
        # Walk directory tree from bottom up to catch nested empty dirs
        for root, dirs, files in os.walk(str(project_path), topdown=False):
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                try:
                    if dir_path.exists() and not any(dir_path.iterdir()):
                        dir_path.rmdir()
                        relative_path = dir_path.relative_to(project_path)
                        removed_dirs.append(str(relative_path))
                        cleanup_log.append(f"📁 Removed empty directory: {relative_path}")
                except OSError:
                    # Directory not empty or permission error - ignore
                    pass
                except Exception as e:
                    self.logger.warning(f"Could not remove empty directory {dir_path}: {e}")
        
        if removed_dirs:
            self.logger.info(f"Removed {len(removed_dirs)} empty directories")
        
        return success
    
    def _remove_directory(self, dir_path: Path, cleanup_log: List[str]) -> bool:
        """Safely remove a directory"""
        try:
            relative_path = dir_path.relative_to(dir_path.parent.parent) if len(dir_path.parts) > 1 else dir_path.name
            shutil.rmtree(dir_path)
            cleanup_log.append(f"📂 Removed directory: {relative_path}")
            self.logger.debug(f"Removed directory: {relative_path}")
            return True
        except PermissionError as e:
            cleanup_log.append(f"❌ Permission denied removing directory: {dir_path.name} - {e}")
            self.logger.error(f"Permission denied removing directory {dir_path}: {e}")
            return False
        except Exception as e:
            cleanup_log.append(f"❌ Failed to remove directory: {dir_path.name} - {e}")
            self.logger.error(f"Failed to remove directory {dir_path}: {e}")
            return False
    
    def _remove_file(self, file_path: Path, cleanup_log: List[str]) -> bool:
        """Safely remove a file"""
        try:
            relative_path = file_path.relative_to(file_path.parent.parent) if len(file_path.parts) > 1 else file_path.name
            file_path.unlink()
            cleanup_log.append(f"📄 Removed file: {relative_path}")
            self.logger.debug(f"Removed file: {relative_path}")
            return True
        except PermissionError as e:
            cleanup_log.append(f"❌ Permission denied removing file: {file_path.name} - {e}")
            self.logger.error(f"Permission denied removing file {file_path}: {e}")
            return False
        except Exception as e:
            cleanup_log.append(f"❌ Failed to remove file: {file_path.name} - {e}")
            self.logger.error(f"Failed to remove file {file_path}: {e}")
            return False
    
    def get_cleanup_preview(self, project_dir: Path) -> Dict[str, List[str]]:
        """
        Preview what would be cleaned without actually cleaning
        
        Returns:
            dict: Dictionary with 'directories', 'files', 'patterns' keys
        """
        project_path = Path(project_dir)
        preview = {
            'directories': [],
            'files': [],
            'patterns': []
        }
        
        # Preview directories
        for dir_name in self.artifact_directories:
            if dir_name.startswith('*'):
                pattern_paths = list(project_path.glob(dir_name))
                for pattern_path in pattern_paths:
                    if pattern_path.is_dir():
                        preview['directories'].append(str(pattern_path.relative_to(project_path)))
            else:
                dir_path = project_path / dir_name
                if dir_path.exists() and dir_path.is_dir():
                    preview['directories'].append(dir_name)
        
        # Preview files
        for file_pattern in self.artifact_files:
            if '*' in file_pattern:
                pattern_paths = list(project_path.glob(file_pattern))
                for pattern_path in pattern_paths:
                    if pattern_path.is_file():
                        preview['files'].append(str(pattern_path.relative_to(project_path)))
            else:
                file_path = project_path / file_pattern
                if file_path.exists() and file_path.is_file():
                    preview['files'].append(file_pattern)
        
        # Preview patterns
        for pattern in self.forbidden_patterns:
            pattern_paths = list(project_path.glob(pattern))
            for pattern_path in pattern_paths:
                preview['patterns'].append(str(pattern_path.relative_to(project_path)))
        
        return preview


def main():
    """Command line interface for project cleaner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean template artifacts from generated project")
    parser.add_argument("project_dir", help="Path to project directory")
    parser.add_argument("--preview", action="store_true", help="Preview what would be cleaned")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    cleaner = ProjectCleaner()
    
    if args.preview:
        preview = cleaner.get_cleanup_preview(Path(args.project_dir))
        print("🔍 Cleanup Preview:")
        
        if preview['directories']:
            print("📂 Directories to remove:")
            for item in preview['directories']:
                print(f"  - {item}")
        
        if preview['files']:
            print("📄 Files to remove:")
            for item in preview['files']:
                print(f"  - {item}")
        
        if preview['patterns']:
            print("🎯 Pattern matches to remove:")
            for item in preview['patterns']:
                print(f"  - {item}")
        
        if not any(preview.values()):
            print("✨ No artifacts found - project is clean")
    else:
        success = cleaner.cleanup_project(Path(args.project_dir))
        exit(0 if success else 1)


if __name__ == "__main__":
    main()
