from frappectl.prompts.common import ask_text, ask_bool, ask_secret


def ask_site_name(default: str | None = None) -> str:
    return ask_text("Site name", default=default)


def ask_admin_password() -> str:
    return ask_secret("Administrator password")


def ask_db_root_password() -> str:
    return ask_secret("MariaDB root password")


def ask_set_default_site(default: bool = True) -> bool:
    return ask_bool("Set as default site?", default=default)
