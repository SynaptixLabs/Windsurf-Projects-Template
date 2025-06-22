#!/usr/bin/env python3
"""
GitHub Manager Library - FINAL HTTPS VERSION v5.5

This version defaults to using HTTPS for remote URLs to avoid SSH key issues.
It ensures maximum compatibility for all users.
"""

import os
import subprocess
import logging
import time
from pathlib import Path
from typing import Optional

class GitHubManager:
    """Manages GitHub repository operations using HTTPS for pushes."""

    def __init__(self):
        self.logger = logging.getLogger('windsurf_generator')

    def create_repository(
        self,
        project_name: str,
        description: str,
        project_dir: Path,
        org: str = "SynaptixLabs",
        private: bool = False,
        auto_commit: bool = True
    ) -> Optional[str]:
        self.logger.info(f"▶️ Starting HTTPS-based GitHub setup for: {project_name}")
        try:
            if not self._initialize_local_repo(project_dir): return None
            repo_url = self._create_remote_repo_on_github(project_name, description, org, private)
            if not repo_url:
                self._provide_manual_github_setup(project_name, org)
                return None
            if not self._link_local_to_remote(project_dir, org, project_name): return None
            if auto_commit and not self._commit_push_and_verify(project_dir, project_name):
                self.logger.error("❌ CRITICAL: The remote repository was created, but the code push failed.")
            self.logger.info(f"✅ GitHub repository setup successful: {repo_url}")
            return repo_url
        except Exception as e:
            self.logger.error(f"❌ An unexpected error occurred during GitHub setup: {e}")
            return None

    def _run_command(self, cmd: list[str], work_dir: Path, description: str, check=True) -> subprocess.CompletedProcess:
        self.logger.info(f"  - {description}...")
        try:
            result = subprocess.run(cmd, cwd=str(work_dir), check=check, capture_output=True, text=True)
            self.logger.info("    ✅ Success")
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"    ❌ FAILED: {description}")
            self.logger.error(f"      STDERR: {e.stderr.strip()}")
            raise

    def _initialize_local_repo(self, project_dir: Path) -> bool:
        self.logger.info("🔧 Step 1: Initializing local Git repository.")
        if (project_dir / ".git").exists():
            self.logger.info("  - Git repository already exists.")
            return True
        try:
            self._run_command(['git', 'init'], project_dir, "Running 'git init'")
            # Set default branch name to 'main'
            self._run_command(['git', 'branch', '-M', 'main'], project_dir, "Setting default branch to 'main'")
            return True
        except subprocess.CalledProcessError:
            return False

    def _create_remote_repo_on_github(self, project_name, description, org, private) -> Optional[str]:
        self.logger.info("🐙 Step 2: Creating remote repository on GitHub.")
        cmd = ['gh', 'repo', 'create', f"{org}/{project_name}", '--description', description]
        cmd.append('--private' if private else '--public')
        try:
            result = self._run_command(cmd, Path.cwd(), "Running 'gh repo create'")
            return result.stdout.strip() or result.stderr.strip()
        except subprocess.CalledProcessError as e:
            if "already exists" in e.stderr.strip().lower():
                repo_url = f"https://github.com/{org}/{project_name}"
                self.logger.info(f"    ✅ Repository already exists on GitHub: {repo_url}")
                return repo_url
            return None

    def _link_local_to_remote(self, project_dir: Path, org: str, project_name: str) -> bool:
        self.logger.info("🔗 Step 3: Linking local and remote repositories.")
        # --- THE KEY CHANGE: USE HTTPS URL ---
        remote_url = f"https://github.com/{org}/{project_name}.git"
        try:
            remotes = self._run_command(['git', 'remote'], project_dir, "Checking existing remotes").stdout
            if 'origin' in remotes.split():
                self._run_command(['git', 'remote', 'set-url', 'origin', remote_url], project_dir, f"Updating remote URL to HTTPS: {remote_url}")
            else:
                self._run_command(['git', 'remote', 'add', 'origin', remote_url], project_dir, f"Adding remote 'origin' with HTTPS URL: {remote_url}")
            return True
        except subprocess.CalledProcessError:
            return False

    def _commit_push_and_verify(self, project_dir: Path, project_name: str) -> bool:
        self.logger.info("🚀 Step 4: Committing, Pushing, and Verifying.")
        try:
            self._run_command(['git', 'config', 'user.name', 'Avidor'], project_dir, "Configuring git user name")
            self._run_command(['git', 'config', 'user.email', 'avidor@synaptixlabs.ai'], project_dir, "Configuring git user email")
            self._run_command(['git', 'add', '.'], project_dir, "Staging all files")
            commit_message = f"🎉 Initial commit: {project_name}"
            self._run_command(['git', 'commit', '--allow-empty', '-m', commit_message], project_dir, "Creating initial commit")
            local_hash = self._run_command(['git', 'rev-parse', 'HEAD'], project_dir, "Getting local commit hash").stdout.strip()
            self._run_command(['git', 'push', '-u', 'origin', 'main'], project_dir, "Pushing to 'main' branch")
            return self._verify_commit_on_remote(project_dir, local_hash)
        except subprocess.CalledProcessError:
            return False

    def _verify_commit_on_remote(self, project_dir: Path, local_commit_hash: str) -> bool:
        self.logger.info("🔍 Step 5: Verifying commit on remote...")
        timeout = 30
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                result = self._run_command(['git', 'ls-remote', 'origin', 'HEAD'], project_dir, "Checking remote HEAD", check=False)
                if result.returncode == 0 and local_commit_hash in result.stdout:
                    self.logger.info("    ✅ VERIFIED: Commit has arrived on remote.")
                    return True
                time.sleep(3)
            except subprocess.CalledProcessError:
                time.sleep(3)
        self.logger.error(f"    ❌ VERIFICATION FAILED: Timeout after {timeout} seconds.")
        return False
        
    def _provide_manual_github_setup(self, project_name, org):
        self.logger.info("📋 Manual GitHub Setup Required:")
        self.logger.info(f"   Create repo manually at: https://github.com/new")
        self.logger.info(f"   Then run: git remote add origin https://github.com/{org}/{project_name}.git && git push -u origin main")