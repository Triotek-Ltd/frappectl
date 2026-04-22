from frappectl.prompts.common import ask_text, ask_choice


def ask_bench_name(default: str | None = None) -> str:
    return ask_text("Bench name", default=default)


def ask_bench_user(default: str | None = None) -> str:
    return ask_text("Bench user", default=default)


def ask_deploy_mode(default: str = "development") -> str:
    return ask_choice("Deployment mode", ["development", "production"], default=default)