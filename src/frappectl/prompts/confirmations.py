import typer


def confirm_action(message: str, default: bool = False) -> bool:
    return typer.confirm(message, default=default)


def confirm_dangerous_action(action_name: str, target: str) -> bool:
    typer.echo(f"Dangerous action: {action_name}")
    typed = typer.prompt(f"Type '{target}' to confirm")
    return typed == target