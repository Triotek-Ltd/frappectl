from frappectl.integrations.shell import run


def create(username: str):
    return run(["useradd", "-m", "-s", "/bin/bash", username])


def ensure_home_permissions(path: str, username: str):
    return run(["chown", "-R", f"{username}:{username}", path])


def generate_ssh_key(username: str, private_key_path: str):
    return run(
        [
            "ssh-keygen",
            "-t",
            "ed25519",
            "-N",
            "",
            "-f",
            private_key_path,
        ],
        user=username,
    )


def git_config(username: str, name: str, email: str):
    run(["git", "config", "--global", "user.name", name], user=username)
    return run(["git", "config", "--global", "user.email", email], user=username)
