from pathlib import Path

from frappectl.core import load_config, save_config, register_bench
from frappectl.integrations import bench
from frappectl.setup.step_helpers import require_root_privileges


def _required(config: dict[str, str], key: str) -> str:
    value = config.get(key, "").strip()
    if not value:
        raise ValueError(f"Missing required config value: {key}")
    return value


def prepare_bench_init(bench_name: str) -> dict[str, str]:
    require_root_privileges("Bench initialization")
    config = load_config(bench_name)
    bench_name_value = _required(config, "BENCH_NAME")
    bench_user = _required(config, "BENCH_USER")
    deploy_mode = _required(config, "DEPLOY_MODE")
    bench_path = _required(config, "BENCH_PATH")
    frappe_branch = _required(config, "FRAPPE_BRANCH")
    python_bin = _required(config, "PYTHON_BIN")

    register_bench(
        bench_name_value,
        {
            "path": bench_path,
            "user": bench_user,
            "mode": deploy_mode,
        },
    )

    bench.install_cli(python_bin=python_bin, user=bench_user)
    version_result = bench.version(user=bench_user)

    target = Path(bench_path)
    if target.exists() and any(target.iterdir()):
        updates = {
            "BENCH_CLI_INSTALLED": "yes",
            "BENCH_CLI_VERSION": version_result.stdout or "unknown",
            "BENCH_INIT_STATUS": "existing",
            "BENCH_ENV_READY": "yes" if (target / "apps" / "frappe").exists() else "no",
        }
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        bench.init(path=bench_path, frappe_branch=frappe_branch, python=python_bin, user=bench_user)
        updates = {
            "BENCH_CLI_INSTALLED": "yes",
            "BENCH_CLI_VERSION": version_result.stdout or "unknown",
            "BENCH_INIT_STATUS": "yes",
            "BENCH_ENV_READY": "yes" if (target / "apps" / "frappe").exists() else "no",
        }

    merged = {**config, **updates}
    save_config(bench_name, merged)
    return merged
