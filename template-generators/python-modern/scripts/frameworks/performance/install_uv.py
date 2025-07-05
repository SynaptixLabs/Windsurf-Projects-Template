# --- Windsurf Metadata ---
# Assistant: Cascade
# Created: 2025-06-28
# Modified: 2025-07-04
# --- End Windsurf Metadata ---

#!/usr/bin/env python3
"""
UV Package Manager Installer (Refactored)
Ensures UV is installed and initializes a virtual environment in the project.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

async def _run_command(cmd: List[str], cwd: Path):
    """Helper to run a shell command asynchronously within a directory."""
    logger.info(f"Executing command: {' '.join(cmd)} in {cwd}")
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd
    )
    stdout_bytes, stderr_bytes = await process.communicate()

    # Decode stdout and stderr safely, stripping leading/trailing whitespace
    stdout = stdout_bytes.decode('utf-8', errors='replace').strip()
    stderr = stderr_bytes.decode('utf-8', errors='replace').strip()

    if process.returncode != 0:
        logger.error(f"Command failed with exit code {process.returncode}")
        if stderr:
            logger.error(f"Stderr: {stderr}")
        raise RuntimeError(f"Command {' '.join(cmd)} failed.")
    
    if stdout:
        logger.info(f"Stdout: {stdout}")

async def _check_uv_installed() -> bool:
    """Checks if UV is available in the shell."""
    logger.info("Checking if UV is installed...")
    try:
        process = await asyncio.create_subprocess_exec(
            'uv', '--version',
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        await process.communicate()
        if process.returncode == 0:
            logger.info("UV is already installed.")
            return True
        else:
            logger.info("UV command failed. Assuming not installed.")
            return False
    except FileNotFoundError:
        logger.info("UV not found. Proceeding with installation.")
        return False

async def _install_uv_globally():
    """Installs UV using the recommended curl/powershell script."""
    logger.info("Installing UV globally...")
    if sys.platform.startswith('win'):
        cmd_str = 'powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"'
    else:
        cmd_str = "curl -LsSf https://astral.sh/uv/install.sh | sh"
    
    process = await asyncio.create_subprocess_shell(
        cmd_str,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout_bytes, stderr_bytes = await process.communicate()

    # Decode stdout and stderr safely, stripping leading/trailing whitespace
    stdout = stdout_bytes.decode('utf-8', errors='replace').strip()
    stderr = stderr_bytes.decode('utf-8', errors='replace').strip()

    if process.returncode != 0:
         if stderr:
            logger.error(f"UV installation script failed with stderr: {stderr}")
         raise RuntimeError(f"UV installation script failed. Command: {cmd_str}")
    
    if stdout:
        logger.info(f"UV installation script finished. Stdout: {stdout}")
    logger.info("UV installed successfully. You may need to restart your shell for the `uv` command to be available in your PATH.")

async def install(project_dir: Path, config: Dict[str, Any]):
    """
    Ensures UV is installed on the system and initializes a project venv.
    """
    logger.info("Setting up UV package manager...")
    try:
        if not await _check_uv_installed():
            await _install_uv_globally()
            # Re-check after installation to confirm it's in the PATH
            if not await _check_uv_installed():
                logger.warning("UV was installed, but it's not available in the current PATH. You may need to restart your terminal or manually add it. Skipping venv creation.")
                return

        logger.info("Initializing UV project environment...")
        python_version = config.get('python_version', '3.12')
        await _run_command(['uv', 'venv', '--python', python_version], cwd=project_dir)
        logger.info(f"UV virtual environment created with Python {python_version}.")
        
        logger.info("UV setup and project initialization complete.")
    except Exception as e:
        logger.error(f"UV setup failed: {e}")
        raise
