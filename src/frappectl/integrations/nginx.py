from frappectl.integrations.shell import run


def test_config():
    return run(["nginx", "-t"], sudo=True)


def reload():
    return run(["systemctl", "reload", "nginx"], sudo=True)


def restart():
    return run(["systemctl", "restart", "nginx"], sudo=True)