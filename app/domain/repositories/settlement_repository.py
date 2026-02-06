"""Settlement repository interface."""
from abc import ABC, abstractmethod
from typing import List
from ..entities.settlement import Settlement


class SettlementRepository(ABC):
    """Abstract interface for settlement data access."""

    @abstractmethod
    def save(self, settlement: Settlement) -> Settlement:
        """Save a settlement payment to database."""
        pass

    @abstractmethod
    def get_by_group(self, group_id: int) -> List[Settlement]:
        """Get all settlements for a group."""
        pass

    @abstractmethod
    def get_all(self) -> List[Settlement]:
        """Get all settlements."""
        pass
