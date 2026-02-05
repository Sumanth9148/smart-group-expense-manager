"""Group repository interface."""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.group import Group


class GroupRepository(ABC):
    """Abstract interface for group data access."""

    @abstractmethod
    def save(self, group: Group) -> Group:
        """Persist a group and return the saved group."""
        pass

    @abstractmethod
    def get_by_id(self, group_id: int) -> Optional[Group]:
        """Fetch a group by id."""
        pass

    @abstractmethod
    def get_all(self) -> List[Group]:
        """Return all groups (read-only)."""
        pass

