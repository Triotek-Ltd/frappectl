from frappectl.core import load_config, save_config
from frappectl.prompts import ask_choice, ask_text, ask_bool


def _require_non_empty(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def collect_backup_settings(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    auto_backup_enabled = existing.get("AUTO_BACKUP_ENABLED")
    if auto_backup_enabled is None:
        auto_backup_enabled = "yes" if ask_bool("Enable automatic backups?", default=True) else "no"

    backup_frequency = existing.get("BACKUP_FREQUENCY")
    if not backup_frequency:
        backup_frequency = ask_choice(
            "Backup frequency",
            ["daily", "twice_daily", "custom"],
            default=existing.get("BACKUP_FREQUENCY", "daily"),
        )

    retention_days = existing.get("BACKUP_RETENTION_DAYS")
    if not retention_days:
        retention_days = _require_non_empty(
            ask_text("Backup retention days", default=existing.get("BACKUP_RETENTION_DAYS", "7")),
            "Backup retention days",
        )

    secondary_backup_mode = existing.get("SECONDARY_BACKUP_MODE")
    if not secondary_backup_mode:
        secondary_backup_mode = ask_choice(
            "Secondary backup destination",
            ["skip", "google_drive", "remote_server"],
            default=existing.get("SECONDARY_BACKUP_MODE", "skip"),
        )

    return {
        "AUTO_BACKUP_ENABLED": auto_backup_enabled,
        "BACKUP_FREQUENCY": backup_frequency,
        "BACKUP_RETENTION_DAYS": retention_days,
        "SECONDARY_BACKUP_MODE": secondary_backup_mode,
    }


def save_backup_settings(bench_name: str, data: dict[str, str]) -> dict[str, str]:
    existing = load_config(bench_name)
    merged = {**existing, **data}
    save_config(bench_name, merged)
    return merged