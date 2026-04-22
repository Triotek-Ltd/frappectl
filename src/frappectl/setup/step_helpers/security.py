from frappectl.core import load_config, save_config
from frappectl.prompts import ask_choice, ask_text, ask_bool


def _require_non_empty(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def collect_security_settings(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    ssh_admin_mode = existing.get("SSH_ADMIN_MODE") or ask_choice(
        "SSH admin key mode",
        ["generate", "existing", "manual_public_key"],
        default=existing.get("SSH_ADMIN_MODE", "generate"),
    )

    admin_ssh_public_key = existing.get("ADMIN_SSH_PUBLIC_KEY", "").strip()
    admin_ssh_private_key_path = existing.get("ADMIN_SSH_PRIVATE_KEY_PATH", "").strip()
    admin_ssh_public_key_path = existing.get("ADMIN_SSH_PUBLIC_KEY_PATH", "").strip()

    if ssh_admin_mode == "manual_public_key" and not admin_ssh_public_key:
        admin_ssh_public_key = _require_non_empty(
            ask_text("Admin SSH public key"),
            "Admin SSH public key",
        )

    if ssh_admin_mode == "existing":
        if not admin_ssh_private_key_path:
            admin_ssh_private_key_path = _require_non_empty(
                ask_text("Existing private key path"),
                "Existing private key path",
            )
        if not admin_ssh_public_key_path:
            admin_ssh_public_key_path = _require_non_empty(
                ask_text("Existing public key path"),
                "Existing public key path",
            )

    disable_root_ssh = existing.get("DISABLE_ROOT_SSH")
    if disable_root_ssh is None:
        disable_root_ssh = "yes" if ask_bool("Disable root SSH login?", default=True) else "no"

    disable_password_ssh = existing.get("DISABLE_PASSWORD_SSH")
    if disable_password_ssh is None:
        disable_password_ssh = "yes" if ask_bool("Disable password SSH authentication?", default=True) else "no"

    enable_fail2ban = existing.get("ENABLE_FAIL2BAN")
    if enable_fail2ban is None:
        enable_fail2ban = "yes" if ask_bool("Enable Fail2ban?", default=True) else "no"

    return {
        "SSH_ADMIN_MODE": ssh_admin_mode,
        "ADMIN_SSH_PUBLIC_KEY": admin_ssh_public_key,
        "ADMIN_SSH_PRIVATE_KEY_PATH": admin_ssh_private_key_path,
        "ADMIN_SSH_PUBLIC_KEY_PATH": admin_ssh_public_key_path,
        "DISABLE_ROOT_SSH": disable_root_ssh,
        "DISABLE_PASSWORD_SSH": disable_password_ssh,
        "ENABLE_FAIL2BAN": enable_fail2ban,
    }


def save_security_settings(bench_name: str, data: dict[str, str]) -> dict[str, str]:
    existing = load_config(bench_name)
    merged = {**existing, **data}
    save_config(bench_name, merged)
    return merged