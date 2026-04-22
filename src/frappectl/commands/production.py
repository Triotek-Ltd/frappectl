import typer

from frappectl.core import resolve_bench, load_config
from frappectl.integrations import nginx, supervisor, systemd
from frappectl.services import prepare_production
from frappectl.setup.step_helpers import require_root_privileges

app = typer.Typer()


@app.command("prepare")
def prepare_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = prepare_production(bench_name)

    typer.echo(f"Production prepared for: {bench_name}")
    typer.echo(f"  PRODUCTION_SETUP_ENABLED={config.get('PRODUCTION_SETUP_ENABLED', '')}")
    typer.echo(f"  PRODUCTION_SETUP_COMPLETE={config.get('PRODUCTION_SETUP_COMPLETE', '')}")
    typer.echo(f"  NGINX_CONFIG_GENERATED={config.get('NGINX_CONFIG_GENERATED', '')}")
    typer.echo(f"  SUPERVISOR_CONFIG_GENERATED={config.get('SUPERVISOR_CONFIG_GENERATED', '')}")


@app.command("status")
def status_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)

    typer.echo(f"Production status for: {bench_name}")
    typer.echo(f"  DEPLOY_MODE={config.get('DEPLOY_MODE', '')}")
    typer.echo(f"  PRODUCTION_SETUP_ENABLED={config.get('PRODUCTION_SETUP_ENABLED', 'unknown')}")
    typer.echo(f"  PRODUCTION_SETUP_COMPLETE={config.get('PRODUCTION_SETUP_COMPLETE', 'unknown')}")
    typer.echo(f"  NGINX_CONFIG_GENERATED={config.get('NGINX_CONFIG_GENERATED', 'unknown')}")
    typer.echo(f"  SUPERVISOR_CONFIG_GENERATED={config.get('SUPERVISOR_CONFIG_GENERATED', 'unknown')}")
    typer.echo(f"  SERVICES_RELOADED={config.get('SERVICES_RELOADED', 'unknown')}")


@app.command("reload-nginx")
def reload_nginx_cmd():
    require_root_privileges("Reload nginx")
    nginx.test_config()
    nginx.reload()
    typer.echo("Nginx configuration tested and reloaded.")


@app.command("restart-supervisor")
def restart_supervisor_cmd():
    require_root_privileges("Restart supervisor")
    supervisor.reread()
    supervisor.update()
    supervisor.restart_all()
    typer.echo("Supervisor reread, update, and restart complete.")


@app.command("safe-restart")
def safe_restart_cmd():
    require_root_privileges("Safe production restart")
    if systemd.is_active("nginx"):
        nginx.test_config()
        nginx.reload()
    if systemd.is_active("supervisor"):
        supervisor.reread()
        supervisor.update()
        supervisor.restart_all()
    typer.echo("Safe restart flow complete.")
