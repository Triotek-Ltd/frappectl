import json
from frappectl.core.paths import bench_state_path


def load_state(bench_name: str) -> dict:
    path = bench_state_path(bench_name)
    if not path.exists():
        return {}

    with open(path, "r") as f:
        return json.load(f)


def save_state(bench_name: str, state: dict):
    path = bench_state_path(bench_name)
    with open(path, "w") as f:
        json.dump(state, f, indent=2)