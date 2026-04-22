import typer

from frappectl.core import resolve_bench, load_config
from frappectl.services import prepare_backup_automation

app = typer.Typer()


@app.command("prepare")
def prepare_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = prepare_backup_automation(bench_name)

    typer.echo(f"Backup automation prepared for: {bench_name}")
    typer.echo(f"  FINAL_HEALTH_CHECK_DONE={config.get('FINAL_HEALTH_CHECK_DONE', '')}")
    typer.echo(f"  FINAL_HEALTH_STATUS={config.get('FINAL_HEALTH_STATUS', '')}")
    typer.echo(f"  BACKUP_AUTOMATION_STATUS={config.get('BACKUP_AUTOMATION_STATUS', '')}")


@app.command("status")
def status_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)

    typer.echo(f"Backup status for: {bench_name}")
    typer.echo(f"  AUTO_BACKUP_ENABLED={config.get('AUTO_BACKUP_ENABLED', '')}")
    typer.echo(f"  BACKUP_FREQUENCY={config.get('BACKUP_FREQUENCY', '')}")
    typer.echo(f"  BACKUP_RETENTION_DAYS={config.get('BACKUP_RETENTION_DAYS', '')}")
    typer.echo(f"  SECONDARY_BACKUP_MODE={config.get('SECONDARY_BACKUP_MODE', '')}")
    typer.echo(f"  BACKUP_AUTOMATION_STATUS={config.get('BACKUP_AUTOMATION_STATUS', 'unknown')}")