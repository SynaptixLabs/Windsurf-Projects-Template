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
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic[email]>=2.0",
        "pydantic-settings>=2.0.0",
        "python-multipart>=0.0.6",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-dotenv>=1.0.0",
        "httpx>=0.25.0",
        "structlog>=23.0.0",
        "sqlalchemy[asyncio]",
        "asyncpg",
        "psutil",
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
        raise RuntimeError(f"FastAPI dependency installation failed. UV Error: {error_message}")

