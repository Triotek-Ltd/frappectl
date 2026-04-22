import os
import platform


def is_linux() -> bool:
    return platform.system().lower() == "linux"


def is_windows() -> bool:
    return os.name == "nt"


def is_supported_dev_platform() -> bool:
    return is_linux() or is_windows()


def is_root() -> bool:
    geteuid = getattr(os, "geteuid", None)
    if geteuid is None:
        return False
    return geteuid() == 0
