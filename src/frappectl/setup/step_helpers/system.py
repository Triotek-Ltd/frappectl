from pathlib import Path

try:
    import pwd
except ImportError:  # pragma: no cover - Windows import guard
    pwd = None

from frappectl.core import ensure_base_dirs
from frappectl.core.constants import (
    BASE_DIR,
    BENCHES_DIR,
    STATE_DIR,
    LOG_DIR,
    INSTALL_ROOT,
    BACKUP_ROOT,
    INSTALL_SCRIPTS_DIR,
    INSTALL_TMP_DIR,
    CRON_DIR,
)
from frappectl.core.errors import PrivilegeError, UnsupportedPlatformError
from frappectl.validators import is_windows, is_linux, is_root


def prepare_installer_directories() -> dict[str, str]:
    ensure_base_dirs()
    for path in [INSTALL_ROOT, BACKUP_ROOT, INSTALL_SCRIPTS_DIR, INSTALL_TMP_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    return {
        "base_dir": str(BASE_DIR),
        "benches_dir": str(BENCHES_DIR),
        "state_dir": str(STATE_DIR),
        "log_dir": str(LOG_DIR),
        "install_root": str(INSTALL_ROOT),
        "backup_root": str(BACKUP_ROOT),
        "scripts_dir": str(INSTALL_SCRIPTS_DIR),
        "tmp_dir": str(INSTALL_TMP_DIR),
        "cron_dir": str(CRON_DIR),
    }


def ensure_directory(path: str) -> str:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def ensure_step_support_directories() -> dict[str, str]:
    return prepare_installer_directories()


def can_apply_real_system_changes() -> bool:
    return is_linux() and is_root()


def require_linux_host() -> None:
    if not is_linux():
        raise UnsupportedPlatformError("Server setup actions are only supported on Linux hosts.")


def require_root_privileges(action: str) -> None:
    require_linux_host()
    if not is_root():
        raise PrivilegeError(f"{action} requires root privileges. Run the CLI with sudo on the server.")


def user_exists(username: str) -> bool:
    if pwd is None:
        return False
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False
