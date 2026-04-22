import typer

from frappectl.commands import (
    setup,
    bench,
    site,
    apps,
    backup,
    update,
    jobs,
    production,
    ssl,
    diagnostics,
    menu,
)

app = typer.Typer(help="Frappe Control CLI")

app.add_typer(setup.app, name="setup")
app.add_typer(bench.app, name="bench")
app.add_typer(site.app, name="site")
app.add_typer(apps.app, name="apps")
app.add_typer(backup.app, name="backup")
app.add_typer(update.app, name="update")
app.add_typer(jobs.app, name="jobs")
app.add_typer(production.app, name="production")
app.add_typer(ssl.app, name="ssl")
app.add_typer(diagnostics.app, name="diagnostics")
app.add_typer(menu.app, name="menu")


def main() -> None:
    app()


@app.callback()
def root(
    bench: str | None = typer.Option(None, "--bench"),
    verbose: bool = typer.Option(False, "--verbose"),
    yes: bool = typer.Option(False, "--yes"),
    non_interactive: bool = typer.Option(False, "--non-interactive"),
) -> None:
    pass