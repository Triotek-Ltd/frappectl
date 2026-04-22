import typer

from frappectl.core import resolve_bench, load_config
from frappectl.integrations import bench as bench_ops
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
