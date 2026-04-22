from frappectl.integrations.shell import run


def update():
    return run(["apt", "update"], sudo=True)


def install(packages: list[str]):
    return run(["apt", "install", "-y"] + packages, sudo=True)