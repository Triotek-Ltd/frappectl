from pathlib import Path

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
from frappectl.prompts import ask_bench_name

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
    bench_name: str | None = typer.Argument(None, help="Bench name"),
):
    target_bench = (bench_name or ask_bench_name()).strip()
    if not target_bench:
        raise ValueError("Bench name is required.")
    _ = get_bench(target_bench)
    set_active_bench(target_bench)
    typer.echo(f"Active bench set to: {target_bench}")


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


@app.command("source")
def source_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    info = get_bench(bench_name)
    config = load_config(bench_name)
    bench_path = Path(info.get("path", "") or config.get("BENCH_PATH", ""))

    typer.echo(f"Bench source info: {bench_name}")
    typer.echo(f"  path={bench_path}")
    typer.echo(f"  benches_root={config.get('BENCHES_ROOT', '')}")
    typer.echo(f"  exists={'yes' if bench_path.exists() else 'no'}")
    typer.echo(f"  apps_dir_exists={'yes' if (bench_path / 'apps').exists() else 'no'}")
    typer.echo(f"  sites_dir_exists={'yes' if (bench_path / 'sites').exists() else 'no'}")
    typer.echo(f"  frappe_branch={config.get('FRAPPE_BRANCH', '')}")
    typer.echo(f"  python_bin={config.get('PYTHON_BIN', '')}")
    typer.echo(f"  deploy_mode={config.get('DEPLOY_MODE', '')}")
    typer.echo(f"  bench_init_status={config.get('BENCH_INIT_STATUS', 'unknown')}")


@app.command("prepare-init")
def prepare_init_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = (bench or ask_bench_name()).strip()
    if not bench_name:
        raise ValueError("Bench name is required.")
    config = prepare_bench_init(bench_name)

    typer.echo(f"Bench init prepared for: {bench_name}")
    typer.echo(f"  BENCH_CLI_INSTALLED={config.get('BENCH_CLI_INSTALLED', '')}")
    typer.echo(f"  BENCH_INIT_STATUS={config.get('BENCH_INIT_STATUS', '')}")


@app.command("start")
def start_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    result = bench_ops.start(path=config.get("BENCH_PATH", ""), user=config.get("BENCH_USER"))
    typer.echo(result.stdout or "Bench start requested.")


@app.command("version")
def version_cmd(
    bench: str | None = typer.Option(None, "--bench", help="Target bench"),
):
    bench_name = resolve_bench(bench)
    config = load_config(bench_name)
    result = bench_ops.version(user=config.get("BENCH_USER"))
    typer.echo(result.stdout or result.stderr)


@app.command("help")
def help_cmd():
    typer.echo("Bench lifecycle commands")
    typer.echo("  bench prepare-init   Initialize bench")
    typer.echo("  bench start          Start bench manually when you explicitly want development mode")
    typer.echo("  bench version        Show bench version")
    typer.echo("  bench source         Show bench source/setup info")
    typer.echo("  bench --help         Show CLI help")


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
