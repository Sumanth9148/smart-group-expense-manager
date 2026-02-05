"""Tests for group service."""

from unittest.mock import Mock
from app.services.group_service import GroupService
from app.domain.entities.group import Group
from app.domain.entities.user import User


def test_add_member():
    """Verify adding a member to a group."""
    group_id = 1
    user_id = 2

    group = Group(group_id, "Test Group")
    user = User(user_id, "Alice", "alice@example.com")

    group_repo = Mock()
    user_repo = Mock()

    group_repo.get_by_id.return_value = group
    user_repo.get_by_id.return_value = user

    service = GroupService(group_repo, user_repo)
    service.add_member(group_id, user_id)

    group_repo.save.assert_called_once()
    assert user in group.members
