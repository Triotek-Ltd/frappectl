import typer

from frappectl.prompts.common import ask_text, ask_choice


def ask_bench_name(default: str | None = None) -> str:
    return ask_text("Bench name", default=default)


def ask_bench_user(default: str | None = None) -> str:
    return ask_text("Bench user", default=default)


def ask_deploy_mode(default: str = "production") -> str:
    return ask_choice("Deployment mode", ["development", "production"], default=default)


def select_bench_name(choices: list[str], default: str | None = None) -> str:
    prompt_text = "Select bench"
    while True:
        typer.echo("Available benches:")
        for item in choices:
            typer.echo(f"  - {item}")
        value = ask_text(prompt_text, default=default).strip()
        if value in choices:
            return value
        typer.echo(f"Invalid bench: {value}")
