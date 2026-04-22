from frappectl.integrations.shell import run


def is_running():
    result = run(["systemctl", "is-active", "mariadb"], check=False)
    return result.stdout == "active"


def start():
    return run(["systemctl", "start", "mariadb"], sudo=True)


def database_exists(name: str, root_password: str | None = None) -> bool:
    cmd = ["mysql", "-u", "root"]
    if root_password:
        cmd.append(f"-p{root_password}")
    cmd.extend(["-Nse", f"SHOW DATABASES LIKE '{name}'"])
    result = run(cmd, check=False)
    return result.returncode == 0 and result.stdout.strip() == name
