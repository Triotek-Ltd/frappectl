import json
from pathlib import Path
from frappectl.core.constants import BENCHES_FILE
from frappectl.core.paths import ensure_base_dirs
from frappectl.core.errors import BenchNotFoundError


def load_registry() -> dict:
    ensure_base_dirs()
    if not BENCHES_FILE.exists():
        return {"benches": {}, "default": None}

    with open(BENCHES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(data: dict):
    ensure_base_dirs()
    with open(BENCHES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def register_bench(name: str, data: dict):
    registry = load_registry()
    registry.setdefault("benches", {})
    registry["benches"][name] = data

    if not registry.get("default"):
        registry["default"] = name

    save_registry(registry)


def unregister_bench(name: str):
    registry = load_registry()
    benches = registry.get("benches", {})
    benches.pop(name, None)

    if registry.get("default") == name:
        registry["default"] = next(iter(benches), None)

    save_registry(registry)


def bench_path_exists(entry: dict) -> bool:
    path = (entry or {}).get("path", "")
    if not path:
        return False
    bench_path = Path(path)
    return bench_path.exists() and any(bench_path.iterdir())


def get_bench(name: str) -> dict:
    registry = load_registry()
    benches = registry.get("benches", {})
    if name not in benches:
        raise BenchNotFoundError(f"Bench '{name}' not found")
    return benches[name]


def list_benches() -> dict:
    return load_registry().get("benches", {})
