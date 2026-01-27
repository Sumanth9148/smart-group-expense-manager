from uuid import uuid4, UUID
from app.domain.entities.group import Group
from app.domain.repositories.group_repository import GroupRepository
from app.domain.repositories.user_repository import UserRepository


class GroupService:

    def __init__(
        self,
        group_repository: GroupRepository,
        user_repository: UserRepository
    ):
        self._group_repository = group_repository
        self._user_repository = user_repository

    def create_group(self, name: str) -> Group:
        group = Group(group_id=uuid4(), name=name)
        self._group_repository.save(group)
        return group

    def add_member(self, group_id: UUID, user_id: UUID) -> None:
        group = self._group_repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        group.add_member(user)
        self._group_repository.save(group)
