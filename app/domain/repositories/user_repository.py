"""User repository interface."""

from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User


class UserRepository(ABC):
    """Abstract interface for user data access."""

    @abstractmethod
    def save(self, user: User) -> User:
        """Persist a user and return the saved user."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by id."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email."""
        pass

    @abstractmethod
    def get_all(self) -> list[User]:
        """Return all users."""
        pass
