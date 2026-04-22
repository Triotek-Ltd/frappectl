from pathlib import PurePosixPath

from frappectl.core import load_config, save_config
from frappectl.core.constants import INSTALL_ROOT, BACKUP_ROOT, BASE_DIR, LOG_DIR
from frappectl.prompts import (
    ask_bench_name,
    ask_bench_user,
    ask_deploy_mode,
    ask_text,
    ask_choice,
    ask_bool,
)
from frappectl.validators import is_valid_bench_name, is_valid_username


def _require_non_empty(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _validate_email(value: str) -> str:
    cleaned = value.strip()
    if not cleaned or "@" not in cleaned or cleaned.startswith("@") or cleaned.endswith("@"):
        raise ValueError("Git email must be a valid non-empty email address")
    return cleaned


def collect_bench_identity(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    actual_bench_name = existing.get("BENCH_NAME") or ask_bench_name(default=bench_name)
    actual_bench_name = actual_bench_name.strip()
    if not is_valid_bench_name(actual_bench_name):
        raise ValueError(f"Invalid bench name: {actual_bench_name}")

    bench_user = existing.get("BENCH_USER") or ask_bench_user()
    bench_user = bench_user.strip()
    if not is_valid_username(bench_user):
        raise ValueError(f"Invalid bench user: {bench_user}")

    deploy_mode = existing.get("DEPLOY_MODE") or ask_deploy_mode()
    deploy_mode = deploy_mode.strip()

    return {
        "BENCH_NAME": actual_bench_name,
        "BENCH_USER": bench_user,
        "DEPLOY_MODE": deploy_mode,
    }


def derive_layout(config: dict[str, str]) -> dict[str, str]:
    bench_name = config["BENCH_NAME"]
    bench_user = config["BENCH_USER"]

    bench_user_home = str(PurePosixPath("/home") / bench_user)
    bench_path = str(PurePosixPath(bench_user_home) / bench_name)

    return {
        "BENCH_USER_HOME": bench_user_home,
        "BENCH_PATH": bench_path,
        "INSTALL_ROOT": str(INSTALL_ROOT),
        "INSTALL_CONFIG_DIR": str(BASE_DIR),
        "INSTALL_LOG_DIR": str(LOG_DIR),
        "BACKUP_ROOT": str(BACKUP_ROOT),
    }


def collect_dev_environment_settings(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    git_user_name = existing.get("GIT_USER_NAME")
    if not git_user_name:
        git_user_name = _require_non_empty(
            ask_text("Git display name", default=existing.get("GIT_USER_NAME", "")),
            "Git display name",
        )

    git_user_email = existing.get("GIT_USER_EMAIL")
    if not git_user_email:
        git_user_email = _validate_email(
            ask_text("Git email", default=existing.get("GIT_USER_EMAIL", ""))
        )

    git_provider = existing.get("GIT_PROVIDER") or ask_choice(
        "Preferred Git provider",
        ["github", "gitlab", "other"],
        default=existing.get("GIT_PROVIDER", "github"),
    )

    private_repo_mode = existing.get("PRIVATE_REPO_MODE") or ask_choice(
        "Private repo access",
        ["public_only", "ssh_key", "deploy_key", "https_token"],
        default=existing.get("PRIVATE_REPO_MODE", "public_only"),
    )

    generate_git_ssh_key = existing.get("GENERATE_GIT_SSH_KEY")
    if generate_git_ssh_key is None:
        generate_git_ssh_key = "yes" if ask_bool(
            "Generate Git SSH key for bench user?",
            default=private_repo_mode in {"ssh_key", "deploy_key"},
        ) else "no"

    return {
        "GIT_USER_NAME": git_user_name.strip(),
        "GIT_USER_EMAIL": git_user_email.strip(),
        "GIT_PROVIDER": git_provider.strip(),
        "PRIVATE_REPO_MODE": private_repo_mode.strip(),
        "GENERATE_GIT_SSH_KEY": generate_git_ssh_key,
    }


def collect_bench_init_settings(bench_name: str) -> dict[str, str]:
    existing = load_config(bench_name)

    frappe_branch = existing.get("FRAPPE_BRANCH") or ask_text(
        "Frappe branch",
        default=existing.get("FRAPPE_BRANCH", "version-16"),
    )
    python_bin = existing.get("PYTHON_BIN") or ask_text(
        "Python executable",
        default=existing.get("PYTHON_BIN", "python3"),
    )

    return {
        "FRAPPE_BRANCH": _require_non_empty(frappe_branch, "Frappe branch"),
        "PYTHON_BIN": _require_non_empty(python_bin, "Python executable"),
    }


def save_bench_identity(bench_name: str, data: dict[str, str]) -> dict[str, str]:
    existing = load_config(bench_name)
    merged = {**existing, **data}
    save_config(bench_name, merged)
    return merged
