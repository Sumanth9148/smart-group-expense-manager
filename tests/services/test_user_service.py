from unittest.mock import Mock
from app.services.user_service import UserService
from app.domain.entities.user import User


def test_create_user():
    user_repo = Mock()
    user_repo.save.return_value = User(id=1, name="Alice", email="alice@example.com")
    service = UserService(user_repo)

    user = service.create_user("Alice")

    user_repo.save.assert_called_once()
    assert user.name == "Alice"
