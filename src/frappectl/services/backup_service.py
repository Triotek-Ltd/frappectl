from pathlib import Path

from frappectl.core import load_config, save_config
from frappectl.core.constants import BACKUP_ROOT, INSTALL_SCRIPTS_DIR, CRON_DIR
from frappectl.setup.step_helpers import finalization_flags, platform_supports_real_service_actions, require_root_privileges
from frappectl.services.health_service import build_health_summary


def _cron_schedule(frequency: str) -> str:
    schedules = {
        "daily": "0 2 * * *",
        "twice_daily": "0 2,14 * * *",
    }
    return schedules.get(frequency, "0 2 * * *")


def prepare_backup_automation(bench_name: str) -> dict[str, str]:
    require_root_privileges("Backup automation setup")
    config = load_config(bench_name)
    flags = finalization_flags()
    bench_user = config.get("BENCH_USER", "").strip()
    bench_path = config.get("BENCH_PATH", "").strip()
    default_site = config.get("DEFAULT_SITE_NAME", "").strip()

    if not all([bench_user, bench_path, default_site]):
        raise ValueError("Backup automation requires BENCH_USER, BENCH_PATH, and DEFAULT_SITE_NAME")

    flags["FINAL_HEALTH_CHECK_DONE"] = "yes"
    health = build_health_summary(bench_name)
    flags["FINAL_HEALTH_STATUS"] = "healthy" if platform_supports_real_service_actions() else "not_run"

    backup_dir = BACKUP_ROOT / bench_name
    backup_dir.mkdir(parents=True, exist_ok=True)
    script_path = INSTALL_SCRIPTS_DIR / f"backup_{bench_name}.sh"
    script_path.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                f"mkdir -p {backup_dir}",
                f"cd {bench_path}",
                (
                    f"sudo -H -u {bench_user} bash -lc "
                    f"'cd {bench_path} && bench --site {default_site} backup --with-files --backup-path {backup_dir}'"
                ),
                f"find {backup_dir} -type f -mtime +{config.get('BACKUP_RETENTION_DAYS', '7')} -delete",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    script_path.chmod(0o750)

    if config.get("AUTO_BACKUP_ENABLED") == "yes":
        cron_path = CRON_DIR / f"frappectl-{bench_name}"
        cron_path.write_text(
            "\n".join(
                [
                    "SHELL=/bin/bash",
                    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                    f"{_cron_schedule(config.get('BACKUP_FREQUENCY', 'daily'))} root {script_path}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        flags["BACKUP_AUTOMATION_STATUS"] = "yes"
    else:
        flags["BACKUP_AUTOMATION_STATUS"] = "disabled"

    flags["BACKUP_SCRIPT_PATH"] = str(script_path)
    flags["BACKUP_DIR"] = str(backup_dir)
    flags["HEALTH_DEFAULT_SITE"] = health.get("default_site", default_site)

    merged = {**config, **flags}
    save_config(bench_name, merged)
    return merged
