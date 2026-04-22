from ..step_helpers import (
    ensure_step_support_directories,
    collect_security_settings,
    save_security_settings,
    prepare_admin_ssh_key_metadata,
    can_apply_real_system_changes,
)
from frappectl.integrations import apt, sshd, systemd
from frappectl.core import save_config


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    security = collect_security_settings(bench_name)
    merged = save_security_settings(bench_name, security)

    generated_paths = prepare_admin_ssh_key_metadata(bench_name)

    if can_apply_real_system_changes():
        if merged["DISABLE_ROOT_SSH"] == "yes":
            sshd.set_option("PermitRootLogin", "no")
        if merged["DISABLE_PASSWORD_SSH"] == "yes":
            sshd.set_option("PasswordAuthentication", "no")
            sshd.set_option("ChallengeResponseAuthentication", "no")
        if merged["ENABLE_FAIL2BAN"] == "yes":
            apt.install(["fail2ban"])
            systemd.enable("fail2ban")
            systemd.start("fail2ban")
            merged["FAIL2BAN_STATUS"] = "yes"
        else:
            merged["FAIL2BAN_STATUS"] = "disabled"
        sshd.reload_service()
        merged["SSH_HARDENING_STATUS"] = "yes"
        save_config(bench_name, merged)
    else:
        merged["FAIL2BAN_STATUS"] = "planned" if merged["ENABLE_FAIL2BAN"] == "yes" else "disabled"
        merged["SSH_HARDENING_STATUS"] = "planned"
        save_config(bench_name, merged)

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

    print(f"  ADMIN_SSH_KEY_STATUS={merged.get('ADMIN_SSH_KEY_STATUS', 'unknown')}")
    print(f"  SSH_HARDENING_STATUS={merged.get('SSH_HARDENING_STATUS', 'unknown')}")
    print(f"  FAIL2BAN_STATUS={merged.get('FAIL2BAN_STATUS', 'unknown')}")
    print(f"  REAL_SYSTEM_CHANGES={'yes' if can_apply_real_system_changes() else 'no'}")
