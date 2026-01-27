from unittest.mock import Mock
from app.services.user_service import UserService


def test_create_user():
    user_repo = Mock()
    service = UserService(user_repo)

    user = service.create_user("Alice")

    user_repo.save.assert_called_once()
    assert user.name == "Alice"
