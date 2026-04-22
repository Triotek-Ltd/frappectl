from ..step_helpers import (
    ensure_step_support_directories,
    collect_dev_environment_settings,
    save_bench_identity,
    can_apply_real_system_changes,
)


def run(bench_name: str) -> None:
    ensure_step_support_directories()

    dev_env = collect_dev_environment_settings(bench_name)
    merged = save_bench_identity(bench_name, dev_env)

    print(f"[{bench_name}] step 04: user & development environment complete")
    print(f"  GIT_USER_NAME={merged['GIT_USER_NAME']}")
    print(f"  GIT_USER_EMAIL={merged['GIT_USER_EMAIL']}")
    print(f"  GIT_PROVIDER={merged['GIT_PROVIDER']}")
    print(f"  PRIVATE_REPO_MODE={merged['PRIVATE_REPO_MODE']}")
    print(f"  GENERATE_GIT_SSH_KEY={merged['GENERATE_GIT_SSH_KEY']}")
    print(f"  REAL_SYSTEM_CHANGES={'yes' if can_apply_real_system_changes() else 'no'}")