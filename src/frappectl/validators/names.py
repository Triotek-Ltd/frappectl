import re


BENCH_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
USERNAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
SITE_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9.-]+$")


def is_valid_bench_name(value: str) -> bool:
    return bool(BENCH_NAME_PATTERN.fullmatch(value))


def is_valid_username(value: str) -> bool:
    return bool(USERNAME_PATTERN.fullmatch(value))


def is_valid_site_name(value: str) -> bool:
    return bool(SITE_NAME_PATTERN.fullmatch(value))