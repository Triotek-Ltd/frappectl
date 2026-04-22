from pathlib import Path

from frappectl.core import load_config, save_config
from frappectl.integrations import bench, mariadb, nginx, redis, supervisor, systemd
from frappectl.setup.step_helpers import (
    production_service_flags,
    https_service_flags,
    require_root_privileges,
)


def prepare_production(bench_name: str) -> dict[str, str]:
    require_root_privileges("Production setup")
    config = load_config(bench_name)
    deploy_mode = config.get("DEPLOY_MODE", "production")
    bench_path = config.get("BENCH_PATH", "").strip()
    bench_user = config.get("BENCH_USER", "").strip()
    default_site = config.get("DEFAULT_SITE_NAME", "").strip()

    flags = production_service_flags()

    if deploy_mode != "production":
        merged = {**config, **flags}
        save_config(bench_name, merged)
        return merged

    if not all([bench_path, bench_user, default_site]):
        raise ValueError("Production setup requires BENCH_PATH, BENCH_USER, and DEFAULT_SITE_NAME")

    service_state = {
        "mariadb": mariadb.is_running(),
        "redis-server": redis.is_running(),
        "nginx": systemd.is_active("nginx"),
        "supervisor": systemd.is_active("supervisor"),
    }
    inactive = [name for name, active in service_state.items() if not active]
    if inactive:
        raise RuntimeError(f"Production prerequisites are not active: {', '.join(inactive)}")

    bench.config_toggle("dns_multitenant", True, cwd=bench_path, user=bench_user)
    bench.config_toggle("serve_default_site", True, cwd=bench_path, user=bench_user)
    current_site_path = bench.clear_current_site(bench_path)
    bench.setup_production(bench_user=bench_user, cwd=bench_path)
    bench.setup_nginx(cwd=bench_path, user=bench_user)
    nginx.test_config()
    supervisor.reread()
    supervisor.update()
    nginx.reload()
    supervisor.restart_all()

    nginx_generated = (Path(bench_path) / "config" / "nginx.conf").exists()
    supervisor_generated = (Path(bench_path) / "config" / "supervisor.conf").exists()

    flags.update(
        {
            "PRODUCTION_SETUP_ENABLED": "yes",
            "PRODUCTION_SETUP_COMPLETE": "yes",
            "NGINX_CONFIG_GENERATED": "yes" if nginx_generated else "no",
            "NGINX_CONFIG_TESTED": "yes",
            "NGINX_RELOADED": "yes",
            "SUPERVISOR_CONFIG_GENERATED": "yes" if supervisor_generated else "no",
            "SUPERVISOR_REREAD_DONE": "yes",
            "SUPERVISOR_UPDATED": "yes",
            "SERVICES_RELOADED": "yes",
            "PRODUCTION_PROCESSES_ACTIVE": "yes",
            "DEFAULT_SITE_PRODUCTION_READY": "yes",
            "MULTITENANT_MODE": "dns",
            "DNS_MULTITENANT_ENABLED": "yes",
            "SERVE_DEFAULT_SITE_ENABLED": "yes",
            "CURRENTSITE_CLEARED": "yes",
            "CURRENTSITE_PATH": str(current_site_path),
        }
    )

    merged = {**config, **flags}
    save_config(bench_name, merged)
    return merged


def prepare_https(bench_name: str) -> dict[str, str]:
    require_root_privileges("HTTPS setup")
    config = load_config(bench_name)
    flags = https_service_flags()
    bench_path = config.get("BENCH_PATH", "").strip()
    bench_user = config.get("BENCH_USER", "").strip()
    default_site = config.get("DEFAULT_SITE_NAME", "").strip()
    ssl_email = config.get("SSL_EMAIL", "").strip()
    dns_ready = config.get("DNS_READY", "no").strip()

    if not all([bench_path, bench_user, default_site, ssl_email]):
        raise ValueError("HTTPS setup requires BENCH_PATH, BENCH_USER, DEFAULT_SITE_NAME, and SSL_EMAIL")

    if dns_ready != "yes":
        flags.update(
            {
                "SSL_ENABLED": "no",
                "SSL_CERT_INSTALLED": "no",
                "HTTPS_REDIRECT_ENABLED": "no",
                "SSL_RENEWAL_ENABLED": "no",
                "SSL_STATUS": "skipped_dns_not_ready",
            }
        )
        merged = {**config, **flags}
        save_config(bench_name, merged)
        return merged

    if default_site.endswith(".local"):
        flags.update(
            {
                "SSL_ENABLED": "no",
                "SSL_CERT_INSTALLED": "no",
                "HTTPS_REDIRECT_ENABLED": "no",
                "SSL_RENEWAL_ENABLED": "no",
                "SSL_STATUS": "skipped_non_public_domain",
            }
        )
        merged = {**config, **flags}
        save_config(bench_name, merged)
        return merged

    bench.setup_letsencrypt(default_site, ssl_email, cwd=bench_path, user=bench_user)
    nginx.reload()

    flags.update(
        {
            "SSL_ENABLED": "yes",
            "SSL_CERT_INSTALLED": "yes",
            "HTTPS_REDIRECT_ENABLED": "yes",
            "SSL_RENEWAL_ENABLED": "yes",
            "SSL_STATUS": "yes",
        }
    )

    merged = {**config, **flags}
    save_config(bench_name, merged)
    return merged
