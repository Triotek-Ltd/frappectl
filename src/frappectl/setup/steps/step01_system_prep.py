from frappectl.core import register_bench, load_config
from ..step_helpers import (
    prepare_installer_directories,
    collect_bench_identity,
    save_bench_identity,
)


def run(bench_name: str) -> None:
    prepare_installer_directories()

    identity = collect_bench_identity(bench_name)
    merged = save_bench_identity(bench_name, identity)

    register_bench(
        merged["BENCH_NAME"],
        {
            "path": load_config(bench_name).get("BENCH_PATH", ""),
            "user": merged["BENCH_USER"],
            "mode": merged["DEPLOY_MODE"],
        },
    )

    print(f"[{bench_name}] step 01: system preparation complete")
    print(f"  BENCH_NAME={merged['BENCH_NAME']}")
    print(f"  BENCH_USER={merged['BENCH_USER']}")
    print(f"  DEPLOY_MODE={merged['DEPLOY_MODE']}")