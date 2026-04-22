import typer

from frappectl.core import resolve_bench, load_state, load_config

app = typer.Typer()


@app.command("open")
def open_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    state = load_state(bench_name)
    config = load_config(bench_name)
    operations = state.get("operations", {})

    typer.echo("Quick Actions")
    typer.echo("=============")
    typer.echo("1. site prepare")
    typer.echo("2. apps prepare-fetch")
    typer.echo("3. production prepare")
    typer.echo("4. jobs health")
    typer.echo("5. backup prepare")
    typer.echo("")
    typer.echo("Bench Operations")
    typer.echo("================")
    typer.echo(f"Bench: {bench_name}")
    typer.echo(f"Operations enabled: {operations.get('operations_menu_enabled', False)}")
    typer.echo(f"Default site: {operations.get('default_site', '') or config.get('DEFAULT_SITE_NAME', '')}")
    typer.echo("")
    typer.echo("1. Bench Lifecycle")
    typer.echo("   bench prepare-init | bench version | bench doctor | bench restart")
    typer.echo("2. App Management")
    typer.echo("   apps plan | apps prepare-fetch | apps list-site")
    typer.echo("3. Default Site and Site Management")
    typer.echo("   site prepare | site list | site migrate | site use")
    typer.echo("4. Backup and Restore")
    typer.echo("   backup prepare | backup status")
    typer.echo("5. Updates, Upgrades, and Maintenance")
    typer.echo("   update plan | site migrate | bench restart")
    typer.echo("6. Scheduler, Workers, and Jobs")
    typer.echo("   jobs health | jobs restart | jobs enable-scheduler | jobs disable-scheduler")
    typer.echo("7. Production and Service Control")
    typer.echo("   production prepare | production reload-nginx | production restart-supervisor | production safe-restart")
    typer.echo("8. Diagnostics and Admin Tools")
    typer.echo("   diagnostics health | bench doctor | bench version")
    typer.echo("9. Dangerous Operations")
    typer.echo("   destructive site actions are not automated yet")
