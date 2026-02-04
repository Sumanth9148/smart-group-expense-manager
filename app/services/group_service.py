from app.domain.entities.group import Group
from app.domain.repositories.group_repository import GroupRepository
from app.domain.repositories.user_repository import UserRepository

import logging
logger = logging.getLogger(__name__)



class GroupService:

    def __init__(
        self,
        group_repository: GroupRepository,
        user_repository: UserRepository
    ):
        self._group_repository = group_repository
        self._user_repository = user_repository

    def create_group(self, name: str) -> Group:
        group = Group(group_id=None, name=name)
        saved = self._group_repository.save(group)
        logger.info(f"Creating group | name={name}")
        return saved

    def add_member(self, group_id: int, user_id: int) -> None:
        group = self._group_repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        group.add_member(user)
        self._group_repository.save(group)

    def remove_member(self, group_id: int, user_id: int) -> None:
        group = self._group_repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        group.remove_member(user)
        self._group_repository.save(group)

    def list_groups(self) -> list[Group]:
        return self._group_repository.get_all()

    def get_group_details(self, group_id: int) -> Group:
        group = self._group_repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        return group
