import typer

from frappectl.core import (
    list_benches,
    get_bench,
    set_active_bench,
    resolve_bench,
    load_config,
)
from frappectl.integrations import bench as bench_ops
from frappectl.services import prepare_bench_init
from frappectl.setup.step_helpers import require_root_privileges

app = typer.Typer()


@app.command("list")
def list_cmd():
    benches = list_benches()
    if not benches:
        typer.echo("No benches registered.")
        return

    for name, data in benches.items():
        typer.echo(
            f"{name} | user={data.get('user', '')} | mode={data.get('mode', '')} | path={data.get('path', '')}"
        )


@app.command("use")
def use_cmd(
    bench_name: str = typer.Argument(..., help="Bench name"),
):
    _ = get_bench(bench_name)
    set_active_bench(bench_name)
    typer.echo(f"Active bench set to: {bench_name}")


@app.command("info")
def info_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    info = get_bench(bench_name)
    config = load_config(bench_name)

    typer.echo(f"Bench: {bench_name}")
    typer.echo(f"  user={info.get('user', '')}")
    typer.echo(f"  mode={info.get('mode', '')}")
    typer.echo(f"  path={info.get('path', '')}")
    typer.echo(f"  frappe_branch={config.get('FRAPPE_BRANCH', '')}")
    typer.echo(f"  python_bin={config.get('PYTHON_BIN', '')}")
    typer.echo(f"  bench_init_status={config.get('BENCH_INIT_STATUS', 'unknown')}")


@app.command("prepare-init")
def prepare_init_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = prepare_bench_init(bench_name)

    typer.echo(f"Bench init prepared for: {bench_name}")
    typer.echo(f"  BENCH_CLI_INSTALLED={config.get('BENCH_CLI_INSTALLED', '')}")
    typer.echo(f"  BENCH_INIT_STATUS={config.get('BENCH_INIT_STATUS', '')}")


@app.command("version")
def version_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    result = bench_ops.version(user=config.get("BENCH_USER"))
    typer.echo(result.stdout or result.stderr)


@app.command("doctor")
def doctor_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    result = bench_ops.doctor(cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(result.stdout or result.stderr)


@app.command("restart")
def restart_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    require_root_privileges("Bench restart")
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    result = bench_ops.restart(cwd=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(result.stdout or "Bench restart requested.")
