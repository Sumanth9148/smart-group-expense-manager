"""User service for business logic."""

import re
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
import logging
logger = logging.getLogger(__name__)


class UserService:
    """Handles user-related operations."""

    def __init__(self, user_repository: UserRepository):
        """Create the service with a user repository."""
        self._user_repository = user_repository

    def create_user(self, name: str, email: str) -> User:
        """Create and save a new user."""
        normalized_name = name.strip()
        normalized_email = email.strip().lower()

        if not normalized_name or not normalized_email:
            raise ValueError("Name and Email cannot be empty")

        if normalized_name[0].isdigit():
            raise ValueError("User name cannot start with a number")

        # Validate email format using regex
        email_pattern = r'^[a-zA-Z][a-zA-Z0-9._-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, normalized_email):
            raise ValueError("Invalid email format. Email must be in format: user@example.com")

        # Validate email uniqueness (case-insensitive)
        existing = self._user_repository.get_by_email(normalized_email)
        if existing:
            return existing

        # Validate name uniqueness (case-insensitive)
        for user in self._user_repository.get_all():
            if user.name.strip().lower() == normalized_name.lower():
                return user

        user = User(id=None, name=normalized_name, email=normalized_email)
        saved = self._user_repository.save(user)
        logger.info(f"Creating user: {saved.name} ({saved.email})")
        return saved

    def get_user(self, user_id: int) -> User | None:
        """Return a user by id if found."""
        return self._user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        """Return a user by email if found."""
        return self._user_repository.get_by_email(email.strip().lower())

    def list_users(self) -> list[User]:
        """Return all users."""
        return self._user_repository.get_all()
