from frappectl.integrations.shell import run


def set_option(option: str, value: str):
    script = (
        rf"$path='C:\invalid';"
        if False
        else
        f"path='/etc/ssh/sshd_config'; "
        f"if grep -Eq '^[#[:space:]]*{option}[[:space:]]+' \"$path\"; then "
        f"sed -i -E 's|^[#[:space:]]*{option}[[:space:]].*|{option} {value}|' \"$path\"; "
        f"else printf '\\n{option} {value}\\n' >> \"$path\"; fi"
    )
    return run(["bash", "-lc", script], sudo=True)


def reload_service():
    result = run(["systemctl", "reload", "ssh"], sudo=True, check=False)
    if result.returncode == 0:
        return result
    result = run(["systemctl", "reload", "sshd"], sudo=True, check=False)
    if result.returncode == 0:
        return result
    result = run(["systemctl", "restart", "ssh"], sudo=True, check=False)
    if result.returncode == 0:
        return result
    return run(["systemctl", "restart", "sshd"], sudo=True)
