from pathlib import Path

from frappectl.core import load_config, save_config
from frappectl.validators import is_windows


def detect_path_conflicts(paths: dict[str, str]) -> dict[str, bool]:
    return {
        "bench_user_home_exists": Path(paths["BENCH_USER_HOME"]).exists(),
        "bench_path_exists": Path(paths["BENCH_PATH"]).exists(),
    }


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