"""Base interface for split strategies."""

from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.expense import Expense
    from app.domain.entities.user import User


class SplitStrategy(ABC):
    """Defines how an expense is split among users."""
    @abstractmethod
    def split(self, expense: "Expense") -> Dict["User", float]:
        """Return a mapping of user to share amount."""
        pass


