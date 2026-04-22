from ..step_helpers import ensure_step_support_directories
from frappectl.core import load_config, load_state, save_state


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    config = load_config(bench_name)
    current_state = load_state(bench_name)
    current_state["operations"] = {
        "operations_menu_enabled": True,
        "default_site": config.get("DEFAULT_SITE_NAME", ""),
        "bench_name": config.get("BENCH_NAME", bench_name),
    }
    save_state(bench_name, current_state)

    print(f"[{bench_name}] step 11: operations complete")
    print("  OPERATIONS_MENU_ENABLED=yes")
    print(f"  DEFAULT_SITE_NAME={config.get('DEFAULT_SITE_NAME', '')}")