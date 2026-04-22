from frappectl.catalog import AppSelection, resolve_apps, installable_site_apps
from frappectl.core import load_config, save_config
from frappectl.setup.step_helpers import can_apply_real_system_changes


def resolve_app_plan_for_bench(bench_name: str):
    config = load_config(bench_name)

    modules = [
        item.strip()
        for item in config.get("SELECTED_BUSINESS_MODULES", "").split(",")
        if item.strip()
    ]

    return resolve_apps(
        AppSelection(
            industry=config.get("SELECTED_INDUSTRY"),
            business_modules=modules,
        )
    )


def prepare_app_fetch(bench_name: str) -> dict[str, str]:
    plan = resolve_app_plan_for_bench(bench_name)

    final_apps = ",".join(app.name for app in plan.all_apps)
    final_app_branches = ",".join(
        f"{app.name}:{app.branch or 'default'}" for app in plan.all_apps
    )

    config = load_config(bench_name)
    config["FINAL_APPS_LIST"] = final_apps
    config["FINAL_APP_BRANCHES"] = final_app_branches
    config["APPS_FETCH_STATUS"] = "planned" if can_apply_real_system_changes() else "no"
    save_config(bench_name, config)
    return config


def prepare_site_install_apps(bench_name: str) -> dict[str, str]:
    plan = resolve_app_plan_for_bench(bench_name)
    site_apps = installable_site_apps(plan)

    config = load_config(bench_name)
    config["SITE_INSTALL_APPS"] = ",".join(app.name for app in site_apps)
    config["SITE_INSTALL_APP_BRANCHES"] = ",".join(
        f"{app.name}:{app.branch or 'default'}" for app in site_apps
    )
    save_config(bench_name, config)
    return config