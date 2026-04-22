import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


class ShellError(Exception):
    pass


def run(
    cmd: List[str],
    *,
    sudo: bool = False,
    user: Optional[str] = None,
    cwd: Optional[str] = None,
    check: bool = True,
) -> CommandResult:
    """
    Run a system command.

    - normal execution
    - sudo execution
    - run-as-user execution
    """

    final_cmd = cmd.copy()

    if user:
        final_cmd = ["sudo", "-u", user] + final_cmd
    elif sudo:
        final_cmd = ["sudo"] + final_cmd

    process = subprocess.run(
        final_cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )

    result = CommandResult(
        returncode=process.returncode,
        stdout=process.stdout.strip(),
        stderr=process.stderr.strip(),
    )

    if check and result.returncode != 0:
        raise ShellError(f"Command failed: {' '.join(final_cmd)}\n{result.stderr}")

    return result