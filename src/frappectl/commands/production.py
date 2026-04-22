import typer

from frappectl.core import resolve_bench, load_config
from frappectl.services import prepare_production

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