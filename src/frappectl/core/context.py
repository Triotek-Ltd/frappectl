import json
from frappectl.core.constants import DEFAULT_CONTEXT_FILE
from frappectl.core.registry import load_registry
from frappectl.core.errors import NoActiveBenchError


def get_active_bench() -> str:
    if not DEFAULT_CONTEXT_FILE.exists():
        raise NoActiveBenchError("No active bench set")

    with open(DEFAULT_CONTEXT_FILE, "r") as f:
        data = json.load(f)

    return data.get("current")


def set_active_bench(name: str):
    DEFAULT_CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DEFAULT_CONTEXT_FILE, "w") as f:
        json.dump({"current": name}, f)


def resolve_bench(cli_value: str | None) -> str:
    if cli_value:
        return cli_value

    return get_active_bench()