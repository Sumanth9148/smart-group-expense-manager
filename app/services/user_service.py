"""User service for business logic."""

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
        # Validate email uniqueness
        existing = self._user_repository.get_by_email(email)
        if existing:
            raise ValueError(f"Email '{email}' is already registered")

        user = User(id=None, name=name, email=email)
        saved = self._user_repository.save(user)
        logger.info(f"Creating user: {saved.name} ({saved.email})")
        return saved

    def get_user(self, user_id: int) -> User | None:
        """Return a user by id if found."""
        return self._user_repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        """Return a user by email if found."""
        return self._user_repository.get_by_email(email)

    def list_users(self) -> list[User]:
        """Return all users."""
        return self._user_repository.get_all()
