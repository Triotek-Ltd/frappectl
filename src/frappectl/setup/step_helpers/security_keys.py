from pathlib import PurePosixPath

from frappectl.core import load_config, save_config
from frappectl.integrations import users
from frappectl.setup.step_helpers import can_apply_real_system_changes


def derive_admin_ssh_key_paths(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)
    bench_user = config["BENCH_USER"]

    ssh_dir = PurePosixPath("/home") / bench_user / ".ssh"
    private_key_path = ssh_dir / "id_ed25519"
    public_key_path = ssh_dir / "id_ed25519.pub"

    return {
        "ADMIN_SSH_PRIVATE_KEY_PATH": str(private_key_path),
        "ADMIN_SSH_PUBLIC_KEY_PATH": str(public_key_path),
    }


def prepare_admin_ssh_key_metadata(bench_name: str) -> dict[str, str]:
    config = load_config(bench_name)
    ssh_admin_mode = config.get("SSH_ADMIN_MODE", "generate")

    if ssh_admin_mode != "generate":
        return {}

    paths = derive_admin_ssh_key_paths(bench_name)
    existing = load_config(bench_name)
    merged = {**existing, **paths}
    if can_apply_real_system_changes():
        users.ensure_home_permissions(str(PurePosixPath(paths["ADMIN_SSH_PRIVATE_KEY_PATH"]).parent), config["BENCH_USER"])
        private_key_path = PurePosixPath(paths["ADMIN_SSH_PRIVATE_KEY_PATH"])
        if not private_key_path.exists():
            users.generate_ssh_key(config["BENCH_USER"], str(private_key_path))
        merged["ADMIN_SSH_KEY_STATUS"] = "yes"
    else:
        merged["ADMIN_SSH_KEY_STATUS"] = "planned"

    save_config(bench_name, merged)
    return paths
