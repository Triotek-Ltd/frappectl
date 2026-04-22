from frappectl.core import load_config, save_config, register_bench
from frappectl.setup.step_helpers import can_apply_real_system_changes


def prepare_bench_init(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)

    register_bench(
        config["BENCH_NAME"],
        {
            "path": config.get("BENCH_PATH", ""),
            "user": config["BENCH_USER"],
            "mode": config["DEPLOY_MODE"],
        },
    )

    if can_apply_real_system_changes():
        updates = {
            "BENCH_CLI_INSTALLED": "planned",
            "BENCH_INIT_STATUS": "planned",
        }
    else:
        updates = {
            "BENCH_CLI_INSTALLED": "no",
            "BENCH_INIT_STATUS": "no",
        }

    merged = {**config, **updates}
    save_config(bench_name, merged)
    return merged