from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        """Persist user and return with assigned id."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        pass
