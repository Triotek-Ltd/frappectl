import typer

from frappectl.core import (
    resolve_bench,
    load_config,
    bench_config_path,
    bench_state_path,
    bench_log_path,
)
from frappectl.setup.engine import run_all, run_step, resume, get_status
from frappectl.setup.planner import get_all_steps, get_next_incomplete_step_number

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
    next_step = get_next_incomplete_step_number({"setup": status})
    last_step = status.get("last_step")

    typer.echo(f"Setup status for bench: {bench_name}")
    typer.echo(f"  last_step={last_step if last_step is not None else 'none'}")
    typer.echo(f"  next_step={next_step if next_step is not None else 'complete'}")
    for step in get_all_steps():
        step_state = steps_state.get(str(step.number), {})
        state = step_state.get("status", "pending")
        detail_parts: list[str] = []
        if step_state.get("started_at"):
            detail_parts.append(f"started={step_state['started_at']}")
        if step_state.get("completed_at"):
            detail_parts.append(f"completed={step_state['completed_at']}")
        if step_state.get("failed_at"):
            detail_parts.append(f"failed={step_state['failed_at']}")
        typer.echo(f"{step.number:02d}. {step.title} -> {state}")
        if detail_parts:
            typer.echo(f"    {' | '.join(detail_parts)}")
        if step_state.get("error"):
            typer.echo(f"    error={step_state['error']}")


@app.command("progress")
def setup_progress(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    status = get_status(bench_name)
    steps_state = status.get("steps", {})
    total_steps = len(get_all_steps())
    completed_steps = sum(
        1 for step in get_all_steps() if steps_state.get(str(step.number), {}).get("status") == "done"
    )
    failed_steps = [
        step for step in get_all_steps() if steps_state.get(str(step.number), {}).get("status") == "failed"
    ]
    running_steps = [
        step for step in get_all_steps() if steps_state.get(str(step.number), {}).get("status") == "running"
    ]
    next_step = get_next_incomplete_step_number({"setup": status})

    typer.echo(f"Setup progress for bench: {bench_name}")
    typer.echo(f"  completed_steps={completed_steps}/{total_steps}")
    typer.echo(f"  running_step={running_steps[0].number if running_steps else 'none'}")
    typer.echo(f"  next_step={next_step if next_step is not None else 'complete'}")
    typer.echo(f"  failed_steps={', '.join(str(step.number) for step in failed_steps) if failed_steps else 'none'}")

    for step in failed_steps:
        step_state = steps_state.get(str(step.number), {})
        typer.echo(f"  step_{step.number}_error={step_state.get('error', 'unknown')}")


@app.command("inspect")
def setup_inspect(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    important_keys = [
        "BENCH_NAME",
        "BENCH_USER",
        "BENCH_PATH",
        "DEPLOY_MODE",
        "FRAPPE_BRANCH",
        "PYTHON_BIN",
        "DEFAULT_SITE_NAME",
        "SET_AS_DEFAULT_SITE",
        "DNS_READY",
        "PRODUCTION_SETUP_COMPLETE",
        "SSL_STATUS",
        "FINAL_HEALTH_STATUS",
        "BACKUP_AUTOMATION_STATUS",
    ]

    typer.echo(f"Setup inspect for bench: {bench_name}")
    for key in important_keys:
        if key in config:
            typer.echo(f"  {key}={config.get(key, '')}")


@app.command("files")
def setup_files(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    typer.echo(f"Setup files for bench: {bench_name}")
    typer.echo(f"  config={bench_config_path(bench_name)}")
    typer.echo(f"  state={bench_state_path(bench_name)}")
    typer.echo(f"  log={bench_log_path(bench_name)}")
