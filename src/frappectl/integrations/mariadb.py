from frappectl.integrations.shell import run


def is_running():
    result = run(["systemctl", "is-active", "mariadb"], check=False)
    return result.stdout == "active"


def start():
    return run(["systemctl", "start", "mariadb"], sudo=True)