"""Tests for user service."""

from unittest.mock import Mock
from app.services.user_service import UserService
from app.domain.entities.user import User


def test_create_user():
    """Verify user creation with unique email."""
    user_repo = Mock()
    user_repo.get_by_email.return_value = None
    user_repo.get_all.return_value = []
    user_repo.save.return_value = User(id=1, name="Alice", email="alice@example.com")
    service = UserService(user_repo)

    user = service.create_user("Alice", "alice@example.com")

    user_repo.get_by_email.assert_called_once_with("alice@example.com")
    user_repo.save.assert_called_once()
    assert user.name == "Alice"
    assert user.email == "alice@example.com"