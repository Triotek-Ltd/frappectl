from ..step_helpers import (
    ensure_step_support_directories,
    collect_https_settings,
    save_site_settings,
)
from frappectl.services import prepare_https


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    https_settings = collect_https_settings(bench_name)
    merged_site = save_site_settings(bench_name, https_settings)
    merged_flags = prepare_https(bench_name)

    print(f"[{bench_name}] step 10: https complete")
    print(f"  SSL_EMAIL={merged_site['SSL_EMAIL']}")
    print(f"  DNS_READY={merged_site['DNS_READY']}")
    print(f"  SSL_ENABLED={merged_flags['SSL_ENABLED']}")
    print(f"  SSL_CERT_INSTALLED={merged_flags['SSL_CERT_INSTALLED']}")
    print(f"  HTTPS_REDIRECT_ENABLED={merged_flags['HTTPS_REDIRECT_ENABLED']}")
    print(f"  SSL_RENEWAL_ENABLED={merged_flags['SSL_RENEWAL_ENABLED']}")