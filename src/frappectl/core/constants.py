from pathlib import Path

BASE_DIR = Path("/etc/frappe-installer")
BENCHES_FILE = BASE_DIR / "benches.json"
BENCHES_DIR = BASE_DIR / "benches"
STATE_DIR = BASE_DIR / "state"
LOG_DIR = Path("/var/log/frappe-installer")
INSTALL_ROOT = Path("/opt/frappe-installer")
BACKUP_ROOT = INSTALL_ROOT / "backups"
INSTALL_SCRIPTS_DIR = INSTALL_ROOT / "scripts"
INSTALL_TMP_DIR = INSTALL_ROOT / "tmp"
CRON_DIR = Path("/etc/cron.d")

DEFAULT_CONTEXT_FILE = Path.home() / ".frappectl" / "context.json"
