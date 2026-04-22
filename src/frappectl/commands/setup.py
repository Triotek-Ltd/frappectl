import typer

from frappectl.core import resolve_bench
from frappectl.setup.engine import run_all, run_step, resume, get_status
from frappectl.setup.planner import get_all_steps

app = typer.Typer()


@app.command("run")
def run_setup(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    run_all(bench_name)
    typer.echo(f"Setup run complete for bench: {bench_name}")


@app.command("step")
def run_single_step(
    number: int = typer.Argument(..., help="Step number"),
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    run_step(bench_name, number)
    typer.echo(f"Step {number} complete for bench: {bench_name}")


@app.command("resume")
def resume_setup(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    resume(bench_name)
    typer.echo(f"Setup resume complete for bench: {bench_name}")


@app.command("status")
def setup_status(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    status = get_status(bench_name)
    steps_state = status.get("steps", {})

    typer.echo(f"Setup status for bench: {bench_name}")
    for step in get_all_steps():
        step_state = steps_state.get(str(step.number), {})
        state = step_state.get("status", "pending")
        typer.echo(f"{step.number:02d}. {step.title} -> {state}")