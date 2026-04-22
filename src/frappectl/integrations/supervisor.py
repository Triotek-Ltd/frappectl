from frappectl.integrations.shell import run


def reread():
    return run(["supervisorctl", "reread"], sudo=True)


def update():
    return run(["supervisorctl", "update"], sudo=True)


def restart_all():
    return run(["supervisorctl", "restart", "all"], sudo=True)