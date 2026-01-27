from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from ..entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass
