from pathlib import Path
from frappectl.core.constants import (
    BASE_DIR,
    BENCHES_DIR,
    STATE_DIR,
    LOG_DIR,
)

def ensure_base_dirs():
    for path in [BASE_DIR, BENCHES_DIR, STATE_DIR, LOG_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def bench_config_path(bench_name: str) -> Path:
    ensure_base_dirs()
    return BENCHES_DIR / f"{bench_name}.env"


def bench_state_path(bench_name: str) -> Path:
    ensure_base_dirs()
    return STATE_DIR / f"{bench_name}.json"


def bench_log_path(bench_name: str) -> Path:
    ensure_base_dirs()
    return LOG_DIR / f"{bench_name}.log"
