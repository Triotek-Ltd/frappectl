from frappectl.core import load_config, save_config
from frappectl.setup.step_helpers import (
    production_service_flags,
    https_service_flags,
    platform_supports_real_service_actions,
)


def prepare_production(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)
    deploy_mode = config.get("DEPLOY_MODE", "development")

    flags = production_service_flags()

    if deploy_mode == "production" and platform_supports_real_service_actions():
        flags.update(
            {
                "PRODUCTION_SETUP_ENABLED": "yes",
                "PRODUCTION_SETUP_COMPLETE": "planned",
                "NGINX_CONFIG_GENERATED": "planned",
                "SUPERVISOR_CONFIG_GENERATED": "planned",
                "SERVICES_RELOADED": "planned",
            }
        )
    elif deploy_mode == "production":
        flags.update(
            {
                "PRODUCTION_SETUP_ENABLED": "yes",
                "PRODUCTION_SETUP_COMPLETE": "no",
                "NGINX_CONFIG_GENERATED": "no",
                "SUPERVISOR_CONFIG_GENERATED": "no",
                "SERVICES_RELOADED": "no",
            }
        )

    merged = {**config, **flags}
    save_config(bench_name, merged)
    return merged


def prepare_https(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)
    flags = https_service_flags()

    if platform_supports_real_service_actions():
        flags.update(
            {
                "SSL_ENABLED": "planned",
                "SSL_CERT_INSTALLED": "planned",
                "HTTPS_REDIRECT_ENABLED": "planned",
                "SSL_RENEWAL_ENABLED": "planned",
            }
        )

    merged = {**config, **flags}
    save_config(bench_name, merged)
    return merged