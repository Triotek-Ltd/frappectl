import shlex
from pathlib import Path

from frappectl.core.constants import INSTALL_ROOT
from frappectl.integrations.shell import run


def _user_shell(command: list[str]) -> list[str]:
    return ["bash", "-lc", f"export PATH=\"$HOME/.local/bin:$PATH\" && {shlex.join(command)}"]


def install_cli(python_bin: str = "python3", user: str | None = None):
    venv_path = INSTALL_ROOT / "bench-cli"
    bench_binary = venv_path / "bin" / "bench"
    venv_python = venv_path / "bin" / "python"

    if not venv_python.exists():
        run(["mkdir", "-p", str(venv_path)], sudo=True)
        run([python_bin, "-m", "venv", str(venv_path)], sudo=True)

    run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"], sudo=True)
    result = run([str(venv_python), "-m", "pip", "install", "--upgrade", "frappe-bench"], sudo=True)
    run(["ln", "-sf", str(bench_binary), "/usr/local/bin/bench"], sudo=True)

    if user:
        run(_user_shell(["bench", "--version"]), user=user)
    return result


def init(path: str, frappe_branch: str, python: str = "python3", user: str | None = None):
    cmd = ["bench", "init", path, "--frappe-branch", frappe_branch, "--python", python]
    if user:
        return run(_user_shell(cmd), user=user)
    return run(cmd)


def start(path: str, user: str | None = None):
    cmd = ["bench", "start"]
    if user:
        return run(_user_shell(cmd), cwd=path, user=user)
    return run(cmd, cwd=path)


def version(user: str | None = None):
    cmd = ["bench", "--version"]
    if user:
        return run(_user_shell(cmd), user=user)
    return run(cmd)


def get_app(repo: str, branch: str | None = None, cwd: str | None = None, user: str | None = None):
    cmd = ["bench", "get-app", repo]
    if branch:
        cmd += ["--branch", branch]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def new_site(name: str, admin_password: str, db_root_password: str, cwd: str, user: str | None = None):
    cmd = [
        "bench",
        "new-site",
        name,
        "--admin-password",
        admin_password,
        "--db-root-password",
        db_root_password,
    ]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def use_site(name: str, cwd: str, user: str | None = None):
    cmd = ["bench", "use", name]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def set_default_site(name: str, cwd: str, user: str | None = None):
    cmd = ["bench", "set-default-site", name]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def install_app(site: str, app_name: str, cwd: str, user: str | None = None):
    cmd = ["bench", "--site", site, "install-app", app_name]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def migrate(site: str, cwd: str, user: str | None = None):
    cmd = ["bench", "--site", site, "migrate"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def clear_cache(site: str, cwd: str, user: str | None = None):
    cmd = ["bench", "--site", site, "clear-cache"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def clear_website_cache(site: str, cwd: str, user: str | None = None):
    cmd = ["bench", "--site", site, "clear-website-cache"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def list_sites(cwd: str, user: str | None = None):
    cmd = ["bench", "list-sites"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def list_apps(site: str, cwd: str, user: str | None = None):
    cmd = ["bench", "--site", site, "list-apps"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def setup_production(bench_user: str, cwd: str, user: str | None = None):
    cmd = ["bench", "setup", "production", bench_user]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd, sudo=True)


def setup_nginx(cwd: str, user: str | None = None):
    cmd = ["bench", "setup", "nginx"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def config_toggle(key: str, enabled: bool, cwd: str, user: str | None = None):
    cmd = ["bench", "config", key, "on" if enabled else "off"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def clear_current_site(cwd: str):
    current_site_path = Path(cwd) / "sites" / "currentsite.txt"
    current_site_path.parent.mkdir(parents=True, exist_ok=True)
    current_site_path.write_text("", encoding="utf-8")
    return current_site_path


def setup_letsencrypt(site: str, email: str, cwd: str, user: str | None = None):
    cmd = ["bench", "setup", "lets-encrypt", site]
    input_text = f"{email}\ny\n"
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user, input_text=input_text)
    return run(cmd, cwd=cwd, input_text=input_text)


def doctor(cwd: str, user: str | None = None):
    cmd = ["bench", "doctor"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def update(cwd: str, user: str | None = None):
    cmd = ["bench", "update"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def build(cwd: str, user: str | None = None):
    cmd = ["bench", "build"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def restart(cwd: str, user: str | None = None):
    cmd = ["bench", "restart"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def enable_scheduler(site: str, cwd: str, user: str | None = None):
    cmd = ["bench", "--site", site, "enable-scheduler"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)


def disable_scheduler(site: str, cwd: str, user: str | None = None):
    cmd = ["bench", "--site", site, "disable-scheduler"]
    if user:
        return run(_user_shell(cmd), cwd=cwd, user=user)
    return run(cmd, cwd=cwd)
