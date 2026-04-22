from frappectl.core import load_config, save_config
from frappectl.setup.step_helpers import can_apply_real_system_changes
from frappectl.services.app_service import prepare_site_install_apps


def prepare_site_setup(bench_name: str) -> dict[str, str]:
    config = prepare_site_install_apps(bench_name)

    config["SITE_CREATE_STATUS"] = "planned" if can_apply_real_system_changes() else "no"
    config["SITE_INSTALL_STATUS"] = "planned" if can_apply_real_system_changes() else "no"

    save_config(bench_name, config)
    return config