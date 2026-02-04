from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    id: Optional[int]
    name: str
    email: str
