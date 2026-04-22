from frappectl.integrations.shell import run


def clone(repo: str, dest: str):
    return run(["git", "clone", repo, dest])


def pull(cwd: str):
    return run(["git", "pull"], cwd=cwd)