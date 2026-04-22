from ..step_helpers import (
    ensure_step_support_directories,
    collect_backup_settings,
    save_backup_settings,
)
from frappectl.services import prepare_backup_automation


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    backup_settings = collect_backup_settings(bench_name)
    save_backup_settings(bench_name, backup_settings)

    merged = prepare_backup_automation(bench_name)

    print(f"[{bench_name}] step 12: finalization complete")
    print(f"  FINAL_HEALTH_CHECK_DONE={merged['FINAL_HEALTH_CHECK_DONE']}")
    print(f"  FINAL_HEALTH_STATUS={merged['FINAL_HEALTH_STATUS']}")
    print(f"  AUTO_BACKUP_ENABLED={merged.get('AUTO_BACKUP_ENABLED', 'no')}")
    print(f"  BACKUP_FREQUENCY={merged.get('BACKUP_FREQUENCY', '')}")
    print(f"  BACKUP_RETENTION_DAYS={merged.get('BACKUP_RETENTION_DAYS', '')}")
    print(f"  SECONDARY_BACKUP_MODE={merged.get('SECONDARY_BACKUP_MODE', '')}")
    print(f"  BACKUP_AUTOMATION_STATUS={merged['BACKUP_AUTOMATION_STATUS']}")