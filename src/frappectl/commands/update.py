import typer

from frappectl.core import resolve_bench, load_config

app = typer.Typer()


@app.command("status")
def status_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)

    typer.echo(f"Update status for: {bench_name}")
    typer.echo(f"  BENCH_INIT_STATUS={config.get('BENCH_INIT_STATUS', 'unknown')}")
    typer.echo(f"  APPS_FETCH_STATUS={config.get('APPS_FETCH_STATUS', 'unknown')}")
    typer.echo(f"  SITE_CREATE_STATUS={config.get('SITE_CREATE_STATUS', 'unknown')}")
    typer.echo(f"  SITE_INSTALL_STATUS={config.get('SITE_INSTALL_STATUS', 'unknown')}")


@app.command("plan")
def plan_cmd():
    typer.echo("Update plan")
    typer.echo("  1. prepare backups")
    typer.echo("  2. fetch app changes")
    typer.echo("  3. run migrations")
    typer.echo("  4. rebuild assets")
    typer.echo("  5. reload services")