import typer

from frappectl.core import resolve_bench, load_state

app = typer.Typer()


@app.command("open")
def open_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    state = load_state(bench_name)
    operations = state.get("operations", {})

    typer.echo("Bench Operations")
    typer.echo("================")
    typer.echo(f"Bench: {bench_name}")
    typer.echo(f"Operations enabled: {operations.get('operations_menu_enabled', False)}")
    typer.echo(f"Default site: {operations.get('default_site', '')}")
    typer.echo("")
    typer.echo("1. Bench Lifecycle")
    typer.echo("2. App Management")
    typer.echo("3. Default Site and Site Management")
    typer.echo("4. Backup and Restore")
    typer.echo("5. Updates, Upgrades, and Maintenance")
    typer.echo("6. Scheduler, Workers, and Jobs")
    typer.echo("7. Production and Service Control")
    typer.echo("8. Diagnostics and Admin Tools")
    typer.echo("9. Dangerous Operations")