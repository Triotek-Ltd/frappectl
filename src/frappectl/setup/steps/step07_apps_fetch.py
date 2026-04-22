from ..step_helpers import (
    ensure_step_support_directories,
    collect_app_selection,
    save_app_selection,
)
from frappectl.services import prepare_app_fetch


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    selection = collect_app_selection(bench_name)
    merged = save_app_selection(bench_name, selection)

    config = prepare_app_fetch(bench_name)

    print(f"[{bench_name}] step 07: apps fetch complete")
    print(f"  SELECTED_INDUSTRY={merged['SELECTED_INDUSTRY']}")
    print(f"  SELECTED_BUSINESS_MODULES={merged['SELECTED_BUSINESS_MODULES']}")
    print(f"  FINAL_APPS_LIST={config['FINAL_APPS_LIST']}")
    print(f"  FINAL_APP_BRANCHES={config['FINAL_APP_BRANCHES']}")
    print(f"  APPS_FETCH_STATUS={config['APPS_FETCH_STATUS']}")