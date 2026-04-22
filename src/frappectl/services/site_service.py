from pathlib import Path

from frappectl.core import load_config, save_config
from frappectl.integrations import bench
from frappectl.setup.step_helpers import require_root_privileges
from frappectl.services.app_service import prepare_site_install_apps


def prepare_site_setup(bench_name: str) -> dict[str, str]:
    require_root_privileges("Site setup")
    config = prepare_site_install_apps(bench_name)
    bench_path = config.get("BENCH_PATH", "").strip()
    bench_user = config.get("BENCH_USER", "").strip()
    site_name = config.get("DEFAULT_SITE_NAME", "").strip()
    admin_password = config.get("SITE_ADMIN_PASSWORD", "").strip()
    db_root_password = config.get("DB_ROOT_PASSWORD", "").strip()

    if not all([bench_path, bench_user, site_name, admin_password, db_root_password]):
        raise ValueError("Site setup requires BENCH_PATH, BENCH_USER, DEFAULT_SITE_NAME, SITE_ADMIN_PASSWORD, and DB_ROOT_PASSWORD")

    if not (Path(bench_path) / "sites" / site_name).exists():
        bench.new_site(
            name=site_name,
            admin_password=admin_password,
            db_root_password=db_root_password,
            cwd=bench_path,
            user=bench_user,
        )

    bench.use_site(site_name, cwd=bench_path, user=bench_user)
    if config.get("SET_AS_DEFAULT_SITE", "yes") == "yes":
        bench.set_default_site(site_name, cwd=bench_path, user=bench_user)

    existing_apps_output = bench.list_apps(site_name, cwd=bench_path, user=bench_user).stdout
    existing_apps = {
        line.strip()
        for line in existing_apps_output.splitlines()
        if line.strip()
    }

    installed_apps: list[str] = []
    for app_name in [item.strip() for item in config.get("SITE_INSTALL_APPS", "").split(",") if item.strip()]:
        if app_name not in existing_apps:
            bench.install_app(site=site_name, app_name=app_name, cwd=bench_path, user=bench_user)
        installed_apps.append(app_name)

    bench.migrate(site_name, cwd=bench_path, user=bench_user)
    bench.clear_cache(site_name, cwd=bench_path, user=bench_user)
    bench.clear_website_cache(site_name, cwd=bench_path, user=bench_user)
    sites_result = bench.list_sites(cwd=bench_path, user=bench_user)
    apps_result = bench.list_apps(site_name, cwd=bench_path, user=bench_user)

    config["SITE_CREATE_STATUS"] = "yes"
    config["SITE_INSTALL_STATUS"] = "yes"
    config["DEFAULT_SITE_CREATED"] = "yes"
    config["DEFAULT_SITE_SET"] = "yes" if config.get("SET_AS_DEFAULT_SITE", "yes") == "yes" else "no"
    config["INSTALLED_SITE_APPS"] = ",".join(installed_apps)
    config["SITE_MIGRATED"] = "yes"
    config["SITE_CACHE_CLEARED"] = "yes"
    config["SITE_LIST_OUTPUT"] = sites_result.stdout.replace("\n", "; ")
    config["SITE_APPS_OUTPUT"] = apps_result.stdout.replace("\n", "; ")

    save_config(bench_name, config)
    return config
