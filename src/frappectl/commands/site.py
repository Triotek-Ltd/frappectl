import json
from pathlib import Path

import typer

from frappectl.core import resolve_bench, load_config, save_config
from frappectl.integrations import bench as bench_ops
from frappectl.services import prepare_site_setup
from frappectl.prompts import (
    ask_site_name,
    ask_admin_password,
    ask_db_root_password,
    ask_set_default_site,
    confirm_action,
)

app = typer.Typer()


def _site_context(bench_name: str) -> tuple[dict[str, str], str, str]:
    config = load_config(bench_name)
    bench_path = config.get("BENCH_PATH", "").strip()
    bench_user = config.get("BENCH_USER", "").strip()
    if not bench_path or not bench_user:
        raise ValueError("Site commands require BENCH_PATH and BENCH_USER to be set first.")
    return config, bench_path, bench_user


def _read_current_default_site(bench_path: str, config: dict[str, str]) -> str:
    common_site_config = Path(bench_path) / "sites" / "common_site_config.json"
    if common_site_config.exists():
        try:
            data = json.loads(common_site_config.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        default_site = str(data.get("default_site", "")).strip()
        if default_site:
            return default_site
    return config.get("DEFAULT_SITE_NAME", "").strip()


@app.command("info")
def info_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)

    typer.echo(f"Bench: {bench_name}")
    typer.echo(f"  DEFAULT_SITE_NAME={config.get('DEFAULT_SITE_NAME', '')}")
    typer.echo(f"  SET_AS_DEFAULT_SITE={config.get('SET_AS_DEFAULT_SITE', '')}")
    typer.echo(f"  SITE_CREATE_STATUS={config.get('SITE_CREATE_STATUS', 'unknown')}")
    typer.echo(f"  SITE_INSTALL_STATUS={config.get('SITE_INSTALL_STATUS', 'unknown')}")
    typer.echo(f"  SITE_INSTALL_APPS={config.get('SITE_INSTALL_APPS', '')}")


@app.command("prepare")
def prepare_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = prepare_site_setup(bench_name)

    typer.echo(f"Site setup prepared for: {bench_name}")
    typer.echo(f"  DEFAULT_SITE_NAME={config.get('DEFAULT_SITE_NAME', '')}")
    typer.echo(f"  SITE_CREATE_STATUS={config.get('SITE_CREATE_STATUS', '')}")
    typer.echo(f"  SITE_INSTALL_STATUS={config.get('SITE_INSTALL_STATUS', '')}")
    typer.echo(f"  SITE_INSTALL_APPS={config.get('SITE_INSTALL_APPS', '')}")


@app.command("create")
def create_cmd(
    site_name: str | None = typer.Option(None, "--site", help="Site name"),
    set_default: bool | None = typer.Option(None, "--set-default", help="Set as default site after creation"),
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config, bench_path, bench_user = _site_context(bench_name)

    target_site = (site_name or ask_site_name(default=config.get("DEFAULT_SITE_NAME"))).strip()
    admin_password = ask_admin_password()
    db_root_password = ask_db_root_password()
    set_as_default = set_default if set_default is not None else ask_set_default_site(default=True)

    typer.echo(f"Creating site: {target_site}")
    bench_ops.new_site(
        name=target_site,
        admin_password=admin_password,
        db_root_password=db_root_password,
        cwd=bench_path,
        user=bench_user,
    )

    if set_as_default:
        typer.echo(f"Setting default site: {target_site}")
        bench_ops.set_default_site(target_site, cwd=bench_path, user=bench_user)
        config["DEFAULT_SITE_NAME"] = target_site
        config["SET_AS_DEFAULT_SITE"] = "yes"
        save_config(bench_name, config)
    typer.echo(f"Created site: {target_site}")


@app.command("set-default")
def set_default_cmd(
    site_name: str = typer.Argument(..., help="Site name"),
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config, bench_path, bench_user = _site_context(bench_name)
    bench_ops.set_default_site(site_name, cwd=bench_path, user=bench_user)
    config["DEFAULT_SITE_NAME"] = site_name
    config["SET_AS_DEFAULT_SITE"] = "yes"
    save_config(bench_name, config)
    typer.echo(f"Default site set to: {site_name}")


@app.command("current-default")
def current_default_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config, bench_path, _bench_user = _site_context(bench_name)
    default_site = _read_current_default_site(bench_path, config)
    typer.echo(f"Current default site: {default_site or 'unknown'}")


@app.command("list")
def list_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    result = bench_ops.list_sites(cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(result.stdout or result.stderr)


@app.command("migrate")
def migrate_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
    site_name: str | None = typer.Option(None, "--site", help="Site name"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    target_site = site_name or config.get("DEFAULT_SITE_NAME", "")
    result = bench_ops.migrate(target_site, cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(result.stdout or f"Migrated site: {target_site}")


@app.command("set-config")
def set_config_cmd(
    key: str = typer.Argument(..., help="Config key"),
    value: str = typer.Argument(..., help="Config value"),
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
    site_name: str | None = typer.Option(None, "--site", help="Site name"),
):
    bench_name = resolve_bench(bench)
    config, bench_path, bench_user = _site_context(bench_name)
    target_site = site_name or config.get("DEFAULT_SITE_NAME", "")
    if not target_site:
        raise ValueError("A target site is required. Use --site or set a default site first.")

    if not confirm_action(f"Set config '{key}' on site '{target_site}'?", default=True):
        raise typer.Exit(code=1)

    bench_ops.set_site_config(target_site, key, value, cwd=bench_path, user=bench_user)
    typer.echo(f"Set config on {target_site}: {key}={value}")


@app.command("use")
def use_site_cmd(
    site_name: str = typer.Argument(..., help="Site name"),
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    bench_ops.use_site(site_name, cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(f"Default site context switched to: {site_name}")


@app.command("multitenant-status")
def multitenant_status_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    typer.echo(f"Bench: {bench_name}")
    typer.echo(f"  MULTITENANT_MODE={config.get('MULTITENANT_MODE', 'unknown')}")
    typer.echo(f"  DNS_MULTITENANT_ENABLED={config.get('DNS_MULTITENANT_ENABLED', 'unknown')}")
    typer.echo(f"  SERVE_DEFAULT_SITE_ENABLED={config.get('SERVE_DEFAULT_SITE_ENABLED', 'unknown')}")
    typer.echo(f"  CURRENTSITE_CLEARED={config.get('CURRENTSITE_CLEARED', 'unknown')}")
    typer.echo(f"  CURRENTSITE_PATH={config.get('CURRENTSITE_PATH', '')}")
