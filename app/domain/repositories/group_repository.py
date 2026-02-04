from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.group import Group


class GroupRepository(ABC):

    @abstractmethod
    def save(self, group: Group) -> Group:
        pass

    @abstractmethod
    def get_by_id(self, group_id: int) -> Optional[Group]:
        pass

    @abstractmethod
    def get_all(self) -> List[Group]:
        """
        Returns all groups (read-only).
        Used by background tasks & monitoring.
        """
        pass

