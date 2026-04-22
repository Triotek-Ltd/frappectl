from pathlib import Path

from frappectl.core import load_config, save_config, load_registry
from frappectl.core.errors import ConflictError
from frappectl.validators import is_windows


def detect_path_conflicts(paths: dict[str, str]) -> dict[str, bool]:
    return {
        "bench_user_home_exists": Path(paths["BENCH_USER_HOME"]).exists(),
        "bench_path_exists": Path(paths["BENCH_PATH"]).exists(),
    }


def assert_no_bench_conflicts(
    bench_name: str,
    config: dict[str, str],
    paths: dict[str, str],
    *,
    include_installer_state: bool = True,
) -> None:
    registry = load_registry()
    registered_benches = registry.get("benches", {})

    if bench_name in registered_benches:
        raise ConflictError(
            f"Bench '{bench_name}' is already registered in installer state. "
            "Choose a new bench name or clean the existing installer state first."
        )

    target_path = paths["BENCH_PATH"]
    for existing_name, data in registered_benches.items():
        if data.get("path") == target_path:
            raise ConflictError(
                f"Bench path '{target_path}' is already registered to bench '{existing_name}'."
            )

    if include_installer_state:
        config_path = Path(paths["INSTALL_CONFIG_DIR"]) / "benches" / f"{bench_name}.env"
        state_path = Path(paths["INSTALL_CONFIG_DIR"]) / "state" / f"{bench_name}.json"
        if config_path.exists():
            raise ConflictError(
                f"Installer config for bench '{bench_name}' already exists at '{config_path}'."
            )
        if state_path.exists():
            raise ConflictError(
                f"Installer state for bench '{bench_name}' already exists at '{state_path}'."
            )

    bench_path = Path(target_path)
    if bench_path.exists() and any(bench_path.iterdir()):
        raise ConflictError(
            f"Bench path '{target_path}' already exists and is not empty. "
            "Use a fresh bench name or move/archive the existing bench first."
        )


def save_service_flags(bench_name: str, data: dict[str, str]) -> dict[str, str]:
    existing = load_config(bench_name)
    merged = {**existing, **data}
    save_config(bench_name, merged)
    return merged


def dependency_service_targets() -> dict[str, str]:
    return {
        "MARIADB_SERVICE": "mariadb",
        "REDIS_SERVICE": "redis-server",
        "NGINX_SERVICE": "nginx",
        "SUPERVISOR_SERVICE": "supervisor",
    }


def production_service_flags() -> dict[str, str]:
    return {
        "PRODUCTION_SETUP_ENABLED": "no",
        "PRODUCTION_SETUP_COMPLETE": "no",
        "NGINX_CONFIG_GENERATED": "no",
        "SUPERVISOR_CONFIG_GENERATED": "no",
        "SERVICES_RELOADED": "no",
    }


def https_service_flags() -> dict[str, str]:
    return {
        "SSL_ENABLED": "no",
        "SSL_CERT_INSTALLED": "no",
        "HTTPS_REDIRECT_ENABLED": "no",
        "SSL_RENEWAL_ENABLED": "no",
    }


def finalization_flags() -> dict[str, str]:
    return {
        "FINAL_HEALTH_CHECK_DONE": "no",
        "FINAL_HEALTH_STATUS": "unknown",
        "BACKUP_AUTOMATION_STATUS": "no",
    }


def platform_supports_real_service_actions() -> bool:
    return not is_windows()
