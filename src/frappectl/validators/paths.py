from pathlib import Path


def path_exists(path: str) -> bool:
    return Path(path).exists()


def is_file(path: str) -> bool:
    return Path(path).is_file()


def is_dir(path: str) -> bool:
    return Path(path).is_dir()