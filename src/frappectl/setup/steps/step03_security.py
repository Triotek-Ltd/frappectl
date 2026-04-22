from ..step_helpers import (
    ensure_step_support_directories,
    collect_security_settings,
    save_security_settings,
    prepare_admin_ssh_key_metadata,
    can_apply_real_system_changes,
)


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    security = collect_security_settings(bench_name)
    merged = save_security_settings(bench_name, security)

    generated_paths = prepare_admin_ssh_key_metadata(bench_name)

    print(f"[{bench_name}] step 03: security complete")
    print(f"  SSH_ADMIN_MODE={merged['SSH_ADMIN_MODE']}")
    print(f"  DISABLE_ROOT_SSH={merged['DISABLE_ROOT_SSH']}")
    print(f"  DISABLE_PASSWORD_SSH={merged['DISABLE_PASSWORD_SSH']}")
    print(f"  ENABLE_FAIL2BAN={merged['ENABLE_FAIL2BAN']}")

    if generated_paths:
        print(f"  ADMIN_SSH_PRIVATE_KEY_PATH={generated_paths['ADMIN_SSH_PRIVATE_KEY_PATH']}")
        print(f"  ADMIN_SSH_PUBLIC_KEY_PATH={generated_paths['ADMIN_SSH_PUBLIC_KEY_PATH']}")

    if merged.get("ADMIN_SSH_PUBLIC_KEY"):
        print("  ADMIN_SSH_PUBLIC_KEY=[provided]")

    print(f"  REAL_SYSTEM_CHANGES={'yes' if can_apply_real_system_changes() else 'no'}")