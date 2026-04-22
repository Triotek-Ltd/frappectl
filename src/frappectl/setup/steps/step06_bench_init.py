from ..step_helpers import (
    ensure_step_support_directories,
    collect_bench_init_settings,
    save_bench_identity,
)
from frappectl.services import prepare_bench_init


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    init_settings = collect_bench_init_settings(bench_name)
    save_bench_identity(bench_name, init_settings)

    merged = prepare_bench_init(bench_name)

    print(f"[{bench_name}] step 06: bench initialization complete")
    print(f"  FRAPPE_BRANCH={merged['FRAPPE_BRANCH']}")
    print(f"  PYTHON_BIN={merged['PYTHON_BIN']}")
    print(f"  BENCH_CLI_INSTALLED={merged['BENCH_CLI_INSTALLED']}")
    print(f"  BENCH_INIT_STATUS={merged['BENCH_INIT_STATUS']}")