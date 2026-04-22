import typer

from frappectl.core import resolve_bench
from frappectl.services import build_health_summary

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