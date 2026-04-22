from frappectl.core import load_config


def build_health_summary(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)

    return {
        "bench_name": config.get("BENCH_NAME", bench_name),
        "deploy_mode": config.get("DEPLOY_MODE", ""),
        "default_site": config.get("DEFAULT_SITE_NAME", ""),
        "bench_init_status": config.get("BENCH_INIT_STATUS", "unknown"),
        "apps_fetch_status": config.get("APPS_FETCH_STATUS", "unknown"),
        "site_create_status": config.get("SITE_CREATE_STATUS", "unknown"),
        "site_install_status": config.get("SITE_INSTALL_STATUS", "unknown"),
        "production_setup_complete": config.get("PRODUCTION_SETUP_COMPLETE", "unknown"),
        "ssl_enabled": config.get("SSL_ENABLED", "unknown"),
        "backup_automation_status": config.get("BACKUP_AUTOMATION_STATUS", "unknown"),
    }