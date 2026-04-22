from pathlib import Path

from frappectl.core import ensure_base_dirs
from frappectl.core.constants import BASE_DIR, BENCHES_DIR, STATE_DIR, LOG_DIR
from frappectl.validators import is_windows


def prepare_installer_directories() -> dict[str, str]:
    ensure_base_dirs()

    return {
        "base_dir": str(BASE_DIR),
        "benches_dir": str(BENCHES_DIR),
        "state_dir": str(STATE_DIR),
        "log_dir": str(LOG_DIR),
    }


def ensure_directory(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def ensure_step_support_directories() -> dict[str, str]:
    return prepare_installer_directories()


def can_apply_real_system_changes() -> bool:
    return not is_windows()