import typer

from frappectl.core import resolve_bench, load_config

app = typer.Typer()


@app.command("status")
def status_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)

    typer.echo(f"Jobs status for: {bench_name}")
    typer.echo(f"  DEPLOY_MODE={config.get('DEPLOY_MODE', '')}")
    typer.echo(f"  PRODUCTION_SETUP_COMPLETE={config.get('PRODUCTION_SETUP_COMPLETE', 'unknown')}")
    typer.echo(f"  SUPERVISOR_CONFIG_GENERATED={config.get('SUPERVISOR_CONFIG_GENERATED', 'unknown')}")
    typer.echo(f"  SERVICES_RELOADED={config.get('SERVICES_RELOADED', 'unknown')}")


@app.command("health")
def health_cmd():
    typer.echo("Jobs health checks")
    typer.echo("  - scheduler status")
    typer.echo("  - worker status")
    typer.echo("  - pending jobs")
    typer.echo("  - process restart planning")