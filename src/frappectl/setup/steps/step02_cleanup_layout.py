from frappectl.core import load_config, register_bench
from ..step_helpers import (
    prepare_installer_directories,
    derive_layout,
    save_bench_identity,
    detect_path_conflicts,
)


def run(bench_name: str) -> None:
    prepare_installer_directories()

    config = load_config(bench_name)
    required = ["BENCH_NAME", "BENCH_USER", "DEPLOY_MODE"]
    missing = [key for key in required if not config.get(key)]
    if missing:
        raise ValueError(
            f"Missing required config for step 02: {', '.join(missing)}"
        )

    layout = derive_layout(config)
    merged = save_bench_identity(bench_name, layout)
    conflicts = detect_path_conflicts(layout)

    register_bench(
        config["BENCH_NAME"],
        {
            "path": merged["BENCH_PATH"],
            "user": config["BENCH_USER"],
            "mode": config["DEPLOY_MODE"],
        },
    )

    print(f"[{bench_name}] step 02: cleanup & layout complete")
    print(f"  BENCH_USER_HOME={merged['BENCH_USER_HOME']}")
    print(f"  BENCH_PATH={merged['BENCH_PATH']}")
    print(f"  conflicts={conflicts}")