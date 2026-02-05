"""Group service for business logic."""

from app.domain.entities.group import Group
from app.domain.repositories.group_repository import GroupRepository
from app.domain.repositories.user_repository import UserRepository

import logging
logger = logging.getLogger(__name__)



class GroupService:
    """Handles group-related operations."""

    def __init__(
        self,
        group_repository: GroupRepository,
        user_repository: UserRepository
    ):
        """Create the service with repositories."""
        self._group_repository = group_repository
        self._user_repository = user_repository

    def create_group(self, name: str) -> Group:
        """Create and save a new group."""
        group = Group(group_id=None, name=name)
        saved = self._group_repository.save(group)
        logger.info(f"Creating group | name={name}")
        return saved

    def add_member(self, group_id: int, user_id: int) -> None:
        """Add a user to a group."""
        group = self._group_repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        group.add_member(user)
        self._group_repository.save(group)

    def remove_member(self, group_id: int, user_id: int) -> None:
        """Remove a user from a group."""
        group = self._group_repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        group.remove_member(user)
        self._group_repository.save(group)

    def list_groups(self) -> list[Group]:
        """Return all groups."""
        return self._group_repository.get_all()

    def get_group_details(self, group_id: int) -> Group:
        """Return a group with members and expenses."""
        group = self._group_repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        return group
