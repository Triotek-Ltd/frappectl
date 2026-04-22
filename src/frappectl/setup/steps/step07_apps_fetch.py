from ..step_helpers import (
    ensure_step_support_directories,
)
from frappectl.services import prepare_app_fetch


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    config = prepare_app_fetch(bench_name)

    print(f"[{bench_name}] step 07: apps fetch complete")
    print(f"  FETCH_APPS_MODE={config['FETCH_APPS_MODE']}")
    print(f"  FINAL_APPS_LIST={config['FINAL_APPS_LIST']}")
    print(f"  FINAL_APP_BRANCHES={config['FINAL_APP_BRANCHES']}")
    print(f"  APPS_FETCH_STATUS={config['APPS_FETCH_STATUS']}")
