"""User entity definition."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class User:
    """Represents a user in the system."""
    id: Optional[int]
    name: str
    email: str
