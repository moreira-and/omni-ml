from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
import mlflow

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

# MLflow configuration
MLFLOW_TRACKING_URI = PROJ_ROOT / "mlruns"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass


def read_yaml(path: str):
    import yaml

    yaml_path = PROJ_ROOT / path
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def git(cmd: str) -> str:
    import subprocess

    return subprocess.check_output(cmd.split(), stderr=subprocess.DEVNULL).decode().strip()


def collect_git_metadata() -> dict:
    """Collect git metadata such as commit hash, branch name, and repository URL."""
    """Exemple: mlflow.set_tags(git_info)"""
    try:
        return {
            "git_commit": git("git rev-parse HEAD"),
            "git_branch": git("git rev-parse --abbrev-ref HEAD"),
            "git_repo": git("git config --get remote.origin.url"),
        }
    except Exception:
        return {
            "git_commit": "unknown",
            "git_branch": "unknown",
            "git_repo": "unknown",
        }
