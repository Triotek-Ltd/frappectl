from .shell import run, CommandResult, ShellError

from . import bench
from . import systemd
from . import apt
from . import git
from . import ssh
from . import mariadb
from . import redis
from . import nginx
from . import supervisor
from . import sshd
from . import users

__all__ = [
    # core shell
    "run",
    "CommandResult",
    "ShellError",

    # modules
    "bench",
    "systemd",
    "apt",
    "git",
    "ssh",
    "mariadb",
    "redis",
    "nginx",
    "supervisor",
    "sshd",
    "users",
]
