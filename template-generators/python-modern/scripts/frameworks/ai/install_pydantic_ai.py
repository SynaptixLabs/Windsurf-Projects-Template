# --- Windsurf Metadata ---
# Assistant: Cascade
# Created: 2025-06-28
# Modified: 2025-07-04
# --- End Windsurf Metadata ---

import asyncio
import os
from pathlib import Path
from typing import Dict, Any

async def install(project_dir: Path, config: Dict[str, Any], venv_path: Path):
    """
    Installs dependencies into the project's virtual environment using a robust pathing method.
    """
    env = os.environ.copy()
    venv_scripts_path = venv_path / "Scripts"
    env["PATH"] = str(venv_scripts_path) + os.pathsep + env["PATH"]

    dependencies = [
        "pydantic-ai>=0.1.0",
        "openai>=1.12.0",
        "pydantic>=2.0"
    ]
    
    command = ["uv", "add", *dependencies]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=project_dir,
        env=env
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_message = stderr.decode().strip()
        raise RuntimeError(f"PydanticAI dependency installation failed. UV Error: {error_message}")
