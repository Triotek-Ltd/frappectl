import typer

from frappectl.core import resolve_bench, load_config
from frappectl.integrations import bench as bench_ops, supervisor
from frappectl.services import build_jobs_health
from frappectl.setup.step_helpers import require_root_privileges

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
def health_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    summary = build_jobs_health(bench_name)
    typer.echo(f"Jobs health for: {bench_name}")
    for key, value in summary.items():
        typer.echo(f"  {key}={value}")


@app.command("restart")
def restart_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    require_root_privileges("Restart job processes")
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    bench_ops.restart(cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    supervisor.restart_all()
    typer.echo("Bench and supervisor job processes restarted.")


@app.command("enable-scheduler")
def enable_scheduler_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
    site_name: str | None = typer.Option(None, "--site", help="Site name"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    target_site = site_name or config.get("DEFAULT_SITE_NAME", "")
    bench_ops.enable_scheduler(target_site, cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(f"Scheduler enabled for: {target_site}")


@app.command("disable-scheduler")
def disable_scheduler_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
    site_name: str | None = typer.Option(None, "--site", help="Site name"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    target_site = site_name or config.get("DEFAULT_SITE_NAME", "")
    bench_ops.disable_scheduler(target_site, cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(f"Scheduler disabled for: {target_site}")
