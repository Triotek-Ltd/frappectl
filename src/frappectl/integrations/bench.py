from frappectl.integrations.shell import run


def init(path: str, frappe_branch: str, python: str = "python3", user: str | None = None):
    return run(
        ["bench", "init", path, "--frappe-branch", frappe_branch, "--python", python],
        user=user,
    )


def start(path: str, user: str | None = None):
    return run(["bench", "start"], cwd=path, user=user)


def version(user: str | None = None):
    return run(["bench", "version"], user=user)


def get_app(repo: str, branch: str | None = None, cwd: str | None = None, user: str | None = None):
    cmd = ["bench", "get-app", repo]
    if branch:
        cmd += ["--branch", branch]
    return run(cmd, cwd=cwd, user=user)


def new_site(name: str, admin_password: str, db_root_password: str, cwd: str, user: str | None = None):
    return run(
        [
            "bench",
            "new-site",
            name,
            "--admin-password",
            admin_password,
            "--db-root-password",
            db_root_password,
        ],
        cwd=cwd,
        user=user,
    )