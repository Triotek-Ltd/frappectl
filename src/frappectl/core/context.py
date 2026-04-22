import json
from frappectl.core.constants import DEFAULT_CONTEXT_FILE
from frappectl.core.registry import load_registry
from frappectl.core.errors import NoActiveBenchError
from frappectl.prompts import ask_bench_name, select_bench_name


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

    try:
        active = get_active_bench()
        if active:
            return active
    except NoActiveBenchError:
        pass

    registry = load_registry()
    benches = sorted(registry.get("benches", {}).keys())

    if len(benches) == 1:
        return benches[0]

    if len(benches) > 1:
        default_name = registry.get("default")
        return select_bench_name(benches, default=default_name if default_name in benches else None)

    return ask_bench_name()
