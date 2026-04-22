from ..step_helpers import (
    ensure_step_support_directories,
    collect_dev_environment_settings,
    save_bench_identity,
    can_apply_real_system_changes,
    user_exists,
)
from frappectl.core import load_config, save_config
from frappectl.integrations import users


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    config = load_config(bench_name)
    bench_user = config.get("BENCH_USER", "").strip()
    bench_user_home = config.get("BENCH_USER_HOME", "").strip()

    if not bench_user or not bench_user_home:
        raise ValueError("Step 4 requires BENCH_USER and BENCH_USER_HOME from earlier setup steps")

    user_created = "no"
    if can_apply_real_system_changes() and not user_exists(bench_user):
        users.create(bench_user)
        user_created = "yes"

    if can_apply_real_system_changes():
        users.ensure_home_permissions(bench_user_home, bench_user)

    dev_env = collect_dev_environment_settings(bench_name)
    merged = save_bench_identity(bench_name, dev_env)

    if can_apply_real_system_changes():
        users.git_config(bench_user, merged["GIT_USER_NAME"], merged["GIT_USER_EMAIL"])

        if merged.get("GENERATE_GIT_SSH_KEY") == "yes":
            ssh_dir = f"{bench_user_home}/.ssh"
            private_key = f"{ssh_dir}/id_ed25519"
            from pathlib import Path
            Path(ssh_dir).mkdir(parents=True, exist_ok=True)
            users.ensure_home_permissions(ssh_dir, bench_user)
            if not Path(private_key).exists():
                users.generate_ssh_key(bench_user, private_key)
            merged["GIT_SSH_KEY_PATH"] = private_key
            merged["GIT_SSH_PUBLIC_KEY_PATH"] = f"{private_key}.pub"
            merged["GIT_SSH_KEY_STATUS"] = "yes"
        else:
            merged["GIT_SSH_KEY_STATUS"] = "skipped"

    merged["BENCH_USER_CREATED"] = user_created if can_apply_real_system_changes() else "planned"
    save_config(bench_name, merged)

    print(f"[{bench_name}] step 04: user & development environment complete")
    print(f"  BENCH_USER_CREATED={merged['BENCH_USER_CREATED']}")
    print(f"  GIT_USER_NAME={merged['GIT_USER_NAME']}")
    print(f"  GIT_USER_EMAIL={merged['GIT_USER_EMAIL']}")
    print(f"  GIT_PROVIDER={merged['GIT_PROVIDER']}")
    print(f"  PRIVATE_REPO_MODE={merged['PRIVATE_REPO_MODE']}")
    print(f"  GENERATE_GIT_SSH_KEY={merged['GENERATE_GIT_SSH_KEY']}")
    print(f"  GIT_SSH_KEY_STATUS={merged.get('GIT_SSH_KEY_STATUS', 'unknown')}")
    print(f"  REAL_SYSTEM_CHANGES={'yes' if can_apply_real_system_changes() else 'no'}")
