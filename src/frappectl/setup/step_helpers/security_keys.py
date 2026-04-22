from pathlib import PurePosixPath

from frappectl.core import load_config, save_config
from frappectl.validators import is_windows


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

    if is_windows():
        merged["ADMIN_SSH_KEY_STATUS"] = "planned"
    else:
        merged["ADMIN_SSH_KEY_STATUS"] = "planned"

    save_config(bench_name, merged)
    return paths