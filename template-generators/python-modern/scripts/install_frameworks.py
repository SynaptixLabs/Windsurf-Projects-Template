import asyncio
import logging
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional, Set

import yaml

# --- Start Logging Setup ---
LOG_FILE = Path.cwd() / "logs" / "post_generation_install.log"
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
# --- End Logging Setup ---

logger = logging.getLogger(__name__)


class FrameworkInstallerDispatcher:
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.answers_file = self.project_dir / ".copier-answers.yml"
        self.installers_root = Path(__file__).parent / "frameworks"
        self.venv_path = self.project_dir / ".venv"

    def _load_answers(self) -> Optional[Dict[str, Any]]:
        """Loads answers from the .copier-answers.yml file."""
        if not self.answers_file.exists():
            logger.error(f"[ERROR] Answers file not found at: {self.answers_file}")
            return None
        try:
            with self.answers_file.open("r") as f:
                answers = yaml.safe_load(f)
                logger.info(f"Successfully loaded answers file:\n{yaml.dump(answers)}")
                return answers
        except Exception as e:
            logger.error(f"[ERROR] Failed to load or parse answers file: {e}")
            return None

    def _resolve_frameworks(self, config: Dict[str, Any]) -> Set[str]:
        """
        Resolves the final list of frameworks to install based on user presets.
        """
        logger.info("Resolving framework list from presets...")
        complexity = config.get("complexity_preset", "")
        all_frameworks = {
            "pydantic_ai", "crew_ai", "langchain", "instructor", "llama_index",
            "fastapi", "litestar", "robyn", "streamlit",
            "polars", "duckdb", "pyarrow", "ibis",
            "uv", "ruff", "orjson", "maturin",
            "postgresql", "mongodb", "redis", "sqlite", "chromadb", "pinecone"
        }
        if complexity == "(Admin) Install ALL packages":
            logger.info("Admin mode: Installing all available packages.")
            # We only return installers that actually exist
            existing_installers = set()
            for framework in all_frameworks:
                for subdir in self.installers_root.iterdir():
                    if subdir.is_dir() and (subdir / f"install_{framework}.py").exists():
                        existing_installers.add(framework)
                        break
            logger.info(f"Found {len(existing_installers)} existing installers: {', '.join(sorted(list(existing_installers)))}")
            return existing_installers
        
        # Fallback for other modes
        selected_frameworks: Set[str] = {"uv", "ruff"}
        focus = config.get("integration_focus", "")
        presets = {
            "ai_first": ["pydantic_ai", "crew_ai", "instructor", "fastapi"],
            "web_api": ["fastapi", "litestar", "pydantic_ai"],
            "data_processing": ["polars", "duckdb", "pyarrow", "ibis"],
            "full_stack": ["fastapi", "pydantic_ai", "polars", "postgresql"],
        }
        if focus in presets:
             selected_frameworks.update(presets[focus])

        logger.info(f"Resolved {len(selected_frameworks)} frameworks: {', '.join(sorted(list(selected_frameworks)))}")
        return selected_frameworks


    async def _run_installer(self, installer_name: str, config: Dict[str, Any], pass_venv_path: bool):
        """
        Dynamically finds, imports, and runs an installer's main function.
        Conditionally passes the venv_path.
        """
        installer_path = None
        for subdir in self.installers_root.iterdir():
            if subdir.is_dir():
                path = subdir / f"install_{installer_name}.py"
                if path.exists():
                    installer_path = path
                    break
        
        if not installer_path:
            logger.warning(f"[WARN] No installer script found for '{installer_name}'. Skipping.")
            return

        try:
            logger.info(f"---> Running installer for: {installer_name}")
            spec = importlib.util.spec_from_file_location(f"framework_installer.{installer_name}", installer_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "install") and asyncio.iscoroutinefunction(module.install):
                # --- THIS IS THE KEY FIX ---
                if pass_venv_path:
                    await module.install(self.project_dir, config, self.venv_path)
                else:
                    await module.install(self.project_dir, config)
                # --- END OF FIX ---
                logger.info(f"---> Successfully ran installer for: {installer_name}")
            else:
                logger.warning(f"[WARN] Installer for '{installer_name}' does not have a valid async 'install' function.")

        except Exception as e:
            logger.error(f"[ERROR] Failed to run installer for '{installer_name}': {e}")
            import traceback
            logger.debug(traceback.format_exc())

    async def dispatch(self):
        """Main dispatcher logic."""
        logger.info("--- Framework Installation Dispatcher Initialized ---")
        config = self._load_answers()
        if not config:
            return

        selected_frameworks = self._resolve_frameworks(config)
        if not selected_frameworks:
            return

        # Prioritize 'uv' installation and call it WITHOUT the venv_path
        if 'uv' in selected_frameworks:
            logger.info("Prioritizing UV installation...")
            await self._run_installer('uv', config, pass_venv_path=False)
            selected_frameworks.remove('uv')

        # Run remaining installers sequentially and pass them the venv_path
        if selected_frameworks:
            logger.info(f"Running remaining {len(selected_frameworks)} installers sequentially...")
            for framework in sorted(list(selected_frameworks)):
                await self._run_installer(framework, config, pass_venv_path=True)
        
        logger.info("--- Framework Installation Dispatcher Finished ---")


def main():
    project_directory = Path.cwd()
    dispatcher = FrameworkInstallerDispatcher(project_directory)
    asyncio.run(dispatcher.dispatch())

if __name__ == "__main__":
    main()
