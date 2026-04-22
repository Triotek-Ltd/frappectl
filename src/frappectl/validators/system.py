import os
import platform


def is_linux() -> bool:
    return platform.system().lower() == "linux"


def is_windows() -> bool:
    return os.name == "nt"


def is_supported_dev_platform() -> bool:
    return is_linux() or is_windows()