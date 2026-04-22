import typer

from frappectl.core import resolve_bench, load_config
from frappectl.services import resolve_app_plan_for_bench, prepare_app_fetch

app = typer.Typer()


@app.command("plan")
def plan_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    plan = resolve_app_plan_for_bench(bench_name)

    typer.echo(f"App plan for: {bench_name}")

    typer.echo("Foundation:")
    for app_def in plan.foundation:
        typer.echo(f"  - {app_def.name} [{app_def.branch or 'default'}]")

    typer.echo("Business:")
    for app_def in plan.business:
        typer.echo(f"  - {app_def.name} [{app_def.branch or 'default'}]")

    typer.echo("Vertical:")
    for app_def in plan.vertical:
        typer.echo(f"  - {app_def.name} [{app_def.branch or 'default'}]")


@app.command("prepare-fetch")
def prepare_fetch_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = prepare_app_fetch(bench_name)

    typer.echo(f"Apps fetch prepared for: {bench_name}")
    typer.echo(f"  FINAL_APPS_LIST={config.get('FINAL_APPS_LIST', '')}")
    typer.echo(f"  FINAL_APP_BRANCHES={config.get('FINAL_APP_BRANCHES', '')}")
    typer.echo(f"  APPS_FETCH_STATUS={config.get('APPS_FETCH_STATUS', '')}")


@app.command("status")
def status_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)

    typer.echo(f"Apps status for: {bench_name}")
    typer.echo(f"  SELECTED_INDUSTRY={config.get('SELECTED_INDUSTRY', '')}")
    typer.echo(f"  SELECTED_BUSINESS_MODULES={config.get('SELECTED_BUSINESS_MODULES', '')}")
    typer.echo(f"  FINAL_APPS_LIST={config.get('FINAL_APPS_LIST', '')}")
    typer.echo(f"  APPS_FETCH_STATUS={config.get('APPS_FETCH_STATUS', 'unknown')}")