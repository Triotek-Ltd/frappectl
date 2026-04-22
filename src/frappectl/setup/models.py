from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class SetupStep:
    number: int
    key: str
    title: str
    handler: Callable[[str], None]