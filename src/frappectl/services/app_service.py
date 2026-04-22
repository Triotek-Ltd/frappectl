from pathlib import Path
import typer

from frappectl.catalog import AppSelection, resolve_apps, installable_site_apps
from frappectl.core import load_config, save_config
from frappectl.integrations import bench
from frappectl.setup.step_helpers import require_root_privileges


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
    require_root_privileges("App fetch")
    plan = resolve_app_plan_for_bench(bench_name)

    final_apps = ",".join(app.name for app in plan.all_apps)
    final_app_branches = ",".join(
        f"{app.name}:{app.branch or 'default'}" for app in plan.all_apps
    )

    config = load_config(bench_name)
    bench_path = config.get("BENCH_PATH", "").strip()
    bench_user = config.get("BENCH_USER", "").strip()
    if not bench_path or not bench_user:
        raise ValueError("BENCH_PATH and BENCH_USER must be set before fetching apps")

    fetched_apps: list[str] = []
    for app in plan.all_apps:
        if app.name == "frappe":
            continue
        if (Path(bench_path) / "apps" / app.name).exists():
            typer.echo(f"[{bench_name}] app already present: {app.name}")
            fetched_apps.append(app.name)
            continue
        repo = app.repo or app.name
        typer.echo(f"[{bench_name}] fetching app: {app.name} from {repo}")
        bench.get_app(repo=repo, branch=app.branch, cwd=bench_path, user=bench_user)
        fetched_apps.append(app.name)

    config["FINAL_APPS_LIST"] = final_apps
    config["FINAL_APP_BRANCHES"] = final_app_branches
    config["FETCHED_APPS"] = ",".join(fetched_apps)
    config["APPS_FETCH_STATUS"] = "yes"
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
