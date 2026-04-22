from frappectl.core import load_config, save_config
from frappectl.setup.step_helpers import finalization_flags, platform_supports_real_service_actions


def prepare_backup_automation(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)
    flags = finalization_flags()

    flags["FINAL_HEALTH_CHECK_DONE"] = "yes"
    flags["FINAL_HEALTH_STATUS"] = "planned" if platform_supports_real_service_actions() else "not_run"
    flags["BACKUP_AUTOMATION_STATUS"] = (
        "planned" if config.get("AUTO_BACKUP_ENABLED") == "yes" else "disabled"
    )

    merged = {**config, **flags}
    save_config(bench_name, merged)
    return merged