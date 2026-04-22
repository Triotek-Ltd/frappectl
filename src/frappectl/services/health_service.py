from frappectl.core import load_config
from frappectl.integrations import bench, supervisor, systemd


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


def build_jobs_health(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)
    bench_path = config.get("BENCH_PATH", "").strip()
    bench_user = config.get("BENCH_USER", "").strip()
    default_site = config.get("DEFAULT_SITE_NAME", "").strip()

    if not all([bench_path, bench_user]):
        raise ValueError("Jobs health requires BENCH_PATH and BENCH_USER")

    doctor_result = bench.doctor(cwd=bench_path, user=bench_user)
    supervisor_result = supervisor.status()
    nginx_active = systemd.is_active("nginx")
    supervisor_active = systemd.is_active("supervisor")

    return {
        "bench_name": config.get("BENCH_NAME", bench_name),
        "default_site": default_site,
        "doctor": doctor_result.stdout or "ok",
        "supervisor_active": "yes" if supervisor_active else "no",
        "nginx_active": "yes" if nginx_active else "no",
        "supervisor_status": supervisor_result.stdout.replace("\n", "; "),
    }
