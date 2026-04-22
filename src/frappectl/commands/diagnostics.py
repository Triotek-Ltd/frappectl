import typer
from shutil import which

from frappectl.core import resolve_bench
from frappectl.services import build_health_summary
from frappectl.validators import is_linux

app = typer.Typer()


@app.command("health")
def health_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    summary = build_health_summary(bench_name)

    typer.echo(f"Health summary for: {bench_name}")
    for key, value in summary.items():
        typer.echo(f"  {key}={value}")


@app.command("preflight")
def preflight_cmd(
    verbose: bool = typer.Option(False, "--verbose", help="Show extra host detail"),
):
    checks = {
        "linux_host": is_linux(),
        "apt_get": which("apt-get") is not None,
        "python3": which("python3") is not None,
        "pip3": which("pip3") is not None or which("python3") is not None,
        "sudo": which("sudo") is not None,
        "systemctl": which("systemctl") is not None,
        "git": which("git") is not None,
    }

    typer.echo("Installer preflight")
    typer.echo("==================")
    for key, value in checks.items():
        typer.echo(f"  {key}={'yes' if value else 'no'}")

    if verbose:
        typer.echo("")
        typer.echo("Detected commands")
        typer.echo("=================")
        for command in ("apt-get", "python3", "pip3", "sudo", "systemctl", "git"):
            typer.echo(f"  {command}={which(command) or 'missing'}")

    failed = [key for key, value in checks.items() if not value]
    if failed:
        typer.echo("")
        typer.echo(f"Preflight failed: missing or unsupported prerequisites: {', '.join(failed)}")
        raise typer.Exit(code=1)

    typer.echo("")
    typer.echo("Preflight passed: host looks ready for installer use.")
