from ..step_helpers import (
    ensure_step_support_directories,
    collect_site_settings,
    save_site_settings,
)
from frappectl.services import prepare_site_setup


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    site_settings = collect_site_settings(bench_name)
    merged = save_site_settings(bench_name, site_settings)

    config = prepare_site_setup(bench_name)

    print(f"[{bench_name}] step 08: site setup complete")
    print(f"  DEFAULT_SITE_NAME={merged['DEFAULT_SITE_NAME']}")
    print(f"  SET_AS_DEFAULT_SITE={merged['SET_AS_DEFAULT_SITE']}")
    print(f"  SITE_INSTALL_APPS={config['SITE_INSTALL_APPS']}")
    print(f"  SITE_INSTALL_APP_BRANCHES={config['SITE_INSTALL_APP_BRANCHES']}")
    print(f"  SITE_CREATE_STATUS={config['SITE_CREATE_STATUS']}")
    print(f"  SITE_INSTALL_STATUS={config['SITE_INSTALL_STATUS']}")