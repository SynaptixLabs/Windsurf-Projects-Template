# --- Windsurf Metadata ---
# Assistant: Cascade
# Created: 2025-06-28
# Modified: 2025-04-12
# --- End Windsurf Metadata ---

import asyncio
import os
from pathlib import Path
from typing import Dict, Any

# --- MODIFIED: The function signature now accepts 'venv_path' ---
async def install(project_dir: Path, config: Dict[str, Any], venv_path: Path):
    """
    Installs dependencies into the project's virtual environment using a robust pathing method.
    """
    env = os.environ.copy()
    venv_scripts_path = venv_path / "Scripts"
    env["PATH"] = str(venv_scripts_path) + os.pathsep + env["PATH"]

    dependencies = [
        "crewai>=0.28.8",
        "crewai-tools>=0.1.6",
        "langchain-community>=0.0.29",
        "python-dotenv>=1.0.0",
        "openai>=1.12.0"
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
        raise RuntimeError(f"CrewAI dependency installation failed. UV Error: {error_message}")
    else:
        # You can log success if you want, but the dispatcher already does
        pass
