import typer

from frappectl.core import resolve_bench, load_config
from frappectl.services import prepare_site_setup

app = typer.Typer()


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