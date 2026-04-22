from ..step_helpers import ensure_step_support_directories
from frappectl.services import prepare_production


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    merged = prepare_production(bench_name)

    print(f"[{bench_name}] step 09: production complete")
    print(f"  DEPLOY_MODE={merged['DEPLOY_MODE']}")
    print(f"  PRODUCTION_SETUP_ENABLED={merged['PRODUCTION_SETUP_ENABLED']}")
    print(f"  PRODUCTION_SETUP_COMPLETE={merged['PRODUCTION_SETUP_COMPLETE']}")
    print(f"  NGINX_CONFIG_GENERATED={merged['NGINX_CONFIG_GENERATED']}")
    print(f"  SUPERVISOR_CONFIG_GENERATED={merged['SUPERVISOR_CONFIG_GENERATED']}")
    print(f"  SERVICES_RELOADED={merged['SERVICES_RELOADED']}")