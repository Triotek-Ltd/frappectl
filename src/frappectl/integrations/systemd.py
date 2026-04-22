from frappectl.integrations.shell import run


def is_active(service: str) -> bool:
    result = run(["systemctl", "is-active", service], check=False)
    return result.stdout == "active"


def start(service: str):
    return run(["systemctl", "start", service], sudo=True)


def restart(service: str):
    return run(["systemctl", "restart", service], sudo=True)


def enable(service: str):
    return run(["systemctl", "enable", service], sudo=True)