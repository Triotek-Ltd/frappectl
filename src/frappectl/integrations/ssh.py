from frappectl.integrations.shell import run


def run_remote(user: str, host: str, command: str):
    return run(["ssh", f"{user}@{host}", command])


def copy_to_remote(local: str, user: str, host: str, remote: str):
    return run(["scp", local, f"{user}@{host}:{remote}"])