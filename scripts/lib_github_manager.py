#!/usr/bin/env python3
"""
GitHub Manager Library

Handles GitHub repository creation and management with multiple fallback methods.
Consolidated from github_integration.py and enhanced_windsurf_generator_v3.py.
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any


class GitHubManager:
    """Manages GitHub repository operations."""
    
    def __init__(self):
        self.logger = logging.getLogger('github_manager')
    
    def create_repository(
        self,
        project_name: str,
        description: str,
        project_dir: Path,
        org: str = "SynaptixLabs",
        private: bool = False
    ) -> Optional[str]:
        """
        Create GitHub repository with multiple fallback methods.
        
        Args:
            project_name: Name of the repository
            description: Repository description
            project_dir: Local project directory
            org: GitHub organization
            private: Whether to make repository private
            
        Returns:
            Repository URL if successful, None otherwise
        """
        try:
            # Method 1: Try GitHub CLI
            success, repo_url = self._try_github_cli(project_name, description, org, private)
            if success:
                self._setup_git_repository(project_dir, project_name, org)
                return repo_url
            
            # Method 2: Try GitHub API with token
            success, repo_url = self._try_github_api(project_name, description, org, private)
            if success:
                self._setup_git_repository(project_dir, project_name, org)
                return repo_url
            
            # Method 3: Provide manual instructions
            self._provide_manual_github_setup(project_name, description, org, private)
            return None
            
        except Exception as e:
            self.logger.error(f"❌ GitHub repository creation failed: {e}")
            return None
    
    def _try_github_cli(
        self,
        project_name: str,
        description: str,
        org: str,
        private: bool
    ) -> Tuple[bool, Optional[str]]:
        """Try GitHub CLI method."""
        try:
            # Check if GitHub CLI is available
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True, check=False)
            
            if result.returncode != 0:
                self.logger.debug("GitHub CLI not available")
                return False, None
            
            # Check if authenticated
            result = subprocess.run(['gh', 'auth', 'status'], 
                                  capture_output=True, text=True, check=False)
            
            if result.returncode != 0:
                self.logger.debug("GitHub CLI not authenticated")
                return False, None
            
            self.logger.info("🔄 Attempting GitHub repository creation via CLI...")
            
            cmd = [
                'gh', 'repo', 'create', f"{org}/{project_name}",
                '--description', description,
                '--add-readme'
            ]
            
            if private:
                cmd.append('--private')
            else:
                cmd.append('--public')
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                repo_url = f"https://github.com/{org}/{project_name}"
                self.logger.info(f"✅ GitHub repository created via CLI: {repo_url}")
                return True, repo_url
            else:
                error_msg = result.stderr.strip()
                if "already exists" in error_msg.lower():
                    repo_url = f"https://github.com/{org}/{project_name}"
                    self.logger.info(f"ℹ️ Repository already exists: {repo_url}")
                    return True, repo_url
                else:
                    self.logger.debug(f"GitHub CLI failed: {error_msg}")
                    return False, None
                    
        except FileNotFoundError:
            self.logger.debug("GitHub CLI not found in PATH")
            return False, None
        except Exception as e:
            self.logger.debug(f"GitHub CLI error: {e}")
            return False, None
    
    def _try_github_api(
        self,
        project_name: str,
        description: str,
        org: str,
        private: bool
    ) -> Tuple[bool, Optional[str]]:
        """Try GitHub API method."""
        try:
            import requests
        except ImportError:
            self.logger.debug("requests library not available")
            return False, None
        
        token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        if not token:
            self.logger.debug("No GitHub token found in environment")
            return False, None
        
        try:
            self.logger.info("🔄 Attempting GitHub repository creation via API...")
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/vnd.github.v3+json',
                'X-GitHub-Api-Version': '2022-11-28'
            }
            
            url = f"https://api.github.com/orgs/{org}/repos"
            data = {
                'name': project_name,
                'description': description,
                'private': private,
                'auto_init': True
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 201:
                repo_data = response.json()
                repo_url = repo_data['html_url']
                self.logger.info(f"✅ GitHub repository created via API: {repo_url}")
                return True, repo_url
            elif response.status_code == 422:
                repo_url = f"https://github.com/{org}/{project_name}"
                self.logger.info(f"ℹ️ Repository might already exist: {repo_url}")
                return True, repo_url
            else:
                self.logger.debug(f"API failed: {response.status_code} - {response.text}")
                return False, None
                
        except Exception as e:
            self.logger.debug(f"GitHub API error: {e}")
            return False, None
    
    def _setup_git_repository(self, project_dir: Path, project_name: str, org: str):
        """Initialize git and set up remote."""
        try:
            original_cwd = os.getcwd()
            os.chdir(project_dir)
            
            # Initialize git if not already done
            if not (project_dir / ".git").exists():
                subprocess.run(['git', 'init'], check=True, capture_output=True)
                self.logger.debug("Git repository initialized")
            
            # Configure user if not set
            try:
                subprocess.run(['git', 'config', 'user.name'], 
                              capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError:
                subprocess.run(['git', 'config', 'user.name', 'Avidor'], 
                              capture_output=True, text=True, check=True)
                
            try:
                subprocess.run(['git', 'config', 'user.email'], 
                              capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError:
                subprocess.run(['git', 'config', 'user.email', 'avidor@synaptixlabs.ai'], 
                              capture_output=True, text=True, check=True)
            
            # Set up remote origin
            remote_url = f"git@github.com:{org}/{project_name}.git"
            
            # Remove existing origin if it exists
            subprocess.run(['git', 'remote', 'remove', 'origin'], 
                          capture_output=True, check=False)
            
            # Add new origin
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], 
                          check=True, capture_output=True)
            
            self.logger.info(f"🔗 Git remote origin set: {remote_url}")
            os.chdir(original_cwd)
            
        except Exception as e:
            self.logger.warning(f"Git setup warning: {e}")
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
    
    def _provide_manual_github_setup(
        self,
        project_name: str,
        description: str,
        org: str,
        private: bool
    ):
        """Provide manual setup instructions."""
        self.logger.info("📋 Manual GitHub repository setup required:")
        self.logger.info(f"   1. Go to: https://github.com/{org}")
        self.logger.info(f"   2. Click 'New repository'")
        self.logger.info(f"   3. Repository name: {project_name}")
        self.logger.info(f"   4. Description: {description}")
        self.logger.info(f"   5. Make it {'private' if private else 'public'} and initialize with README")
        self.logger.info(f"   6. Run: git remote add origin git@github.com:{org}/{project_name}.git")
    
    def check_git_status(self, project_dir: Path) -> Dict[str, Any]:
        """Check current git status of project."""
        status = {
            'git_initialized': False,
            'has_remote': False,
            'remote_url': None,
            'has_commits': False
        }
        
        try:
            original_cwd = os.getcwd()
            os.chdir(project_dir)
            
            # Check if git is initialized
            if (project_dir / ".git").exists():
                status['git_initialized'] = True
                
                # Check for remote
                try:
                    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                          capture_output=True, text=True, check=True)
                    status['has_remote'] = True
                    status['remote_url'] = result.stdout.strip()
                except subprocess.CalledProcessError:
                    pass
                
                # Check for commits
                try:
                    result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                                          capture_output=True, text=True, check=True)
                    status['has_commits'] = bool(result.stdout.strip())
                except subprocess.CalledProcessError:
                    pass
            
            os.chdir(original_cwd)
            
        except Exception as e:
            self.logger.debug(f"Git status check error: {e}")
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
        
        return status
    
    def check_github_cli_available(self) -> bool:
        """Check if GitHub CLI is available and authenticated."""
        try:
            # Check if gh is installed
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True, check=False)
            
            if result.returncode != 0:
                return False
            
            # Check if authenticated
            result = subprocess.run(['gh', 'auth', 'status'], 
                                  capture_output=True, text=True, check=False)
            
            return result.returncode == 0
            
        except FileNotFoundError:
            return False
        except Exception:
            return False
