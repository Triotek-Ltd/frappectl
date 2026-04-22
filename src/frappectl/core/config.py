from pathlib import Path
from frappectl.core.paths import bench_config_path


def load_config(bench_name: str) -> dict:
    path = bench_config_path(bench_name)
    if not path.exists():
        return {}

    data = {}
    with open(path, "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                data[k] = v
    return data


def save_config(bench_name: str, config: dict):
    path = bench_config_path(bench_name)
    with open(path, "w") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")