import typer


def ask_text(message: str, default: str | None = None) -> str:
    return typer.prompt(message, default=default)


def ask_choice(message: str, choices: list[str], default: str | None = None) -> str:
    prompt_text = f"{message} ({', '.join(choices)})"
    while True:
        value = typer.prompt(prompt_text, default=default).strip()
        if value in choices:
            return value
        typer.echo(f"Invalid choice: {value}")


def ask_bool(message: str, default: bool = False) -> bool:
    return typer.confirm(message, default=default)