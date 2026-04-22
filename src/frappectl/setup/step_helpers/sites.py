from frappectl.core import load_config, save_config
from frappectl.prompts import (
    ask_site_name,
    ask_admin_password,
    ask_db_root_password,
    ask_set_default_site,
    ask_text,
    ask_bool,
)
from frappectl.validators import is_valid_site_name


def _require_non_empty(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def collect_site_settings(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    default_site_name = existing.get("DEFAULT_SITE_NAME") or ask_site_name()
    default_site_name = default_site_name.strip()
    if not is_valid_site_name(default_site_name):
        raise ValueError(f"Invalid site name: {default_site_name}")

    site_admin_password = existing.get("SITE_ADMIN_PASSWORD")
    if not site_admin_password:
        site_admin_password = _require_non_empty(
            ask_admin_password(),
            "Administrator password",
        )

    db_root_password = existing.get("DB_ROOT_PASSWORD")
    if not db_root_password:
        db_root_password = _require_non_empty(
            ask_db_root_password(),
            "MariaDB root password",
        )

    set_default_site = existing.get("SET_AS_DEFAULT_SITE")
    if set_default_site is None:
        set_default_site = "yes" if ask_set_default_site(default=True) else "no"

    return {
        "DEFAULT_SITE_NAME": default_site_name,
        "SITE_ADMIN_PASSWORD": site_admin_password,
        "DB_ROOT_PASSWORD": db_root_password,
        "SET_AS_DEFAULT_SITE": set_default_site,
    }


def collect_https_settings(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    ssl_email = existing.get("SSL_EMAIL")
    if not ssl_email:
        ssl_email = _require_non_empty(
            ask_text("SSL email"),
            "SSL email",
        )

    dns_ready = existing.get("DNS_READY")
    if dns_ready is None:
        dns_ready = "yes" if ask_bool("Is DNS already pointing to this server?", default=False) else "no"

    return {
        "SSL_EMAIL": ssl_email.strip(),
        "DNS_READY": dns_ready,
    }


def save_site_settings(bench_name: str, data: dict[str, str]) -> dict[str, str]:
    existing = load_config(bench_name)
    merged = {**existing, **data}
    save_config(bench_name, merged)
    return merged