from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List
from app.domain.entities.group import Group


class GroupRepository(ABC):

    @abstractmethod
    def save(self, group: Group) -> None:
        pass

    @abstractmethod
    def get_by_id(self, group_id: UUID) -> Optional[Group]:
        pass

    @abstractmethod
    def get_all(self) -> List[Group]:
        """
        Returns all groups (read-only).
        Used by background tasks & monitoring.
        """
        pass

