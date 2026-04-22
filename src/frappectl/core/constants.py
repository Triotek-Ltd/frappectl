from pathlib import Path

BASE_DIR = Path("/etc/frappe-installer")
BENCHES_FILE = BASE_DIR / "benches.json"
BENCHES_DIR = BASE_DIR / "benches"
STATE_DIR = BASE_DIR / "state"
LOG_DIR = Path("/var/log/frappe-installer")

DEFAULT_CONTEXT_FILE = Path.home() / ".frappectl" / "context.json"