from uuid import UUID
from typing import List
from .user import User
from .expense import Expense


class Group:
    def __init__(self, group_id: UUID, name: str):
        self.id = group_id
        self.name = name
        self._members: List[User] = []
        self._expenses: List[Expense] = []

    def add_member(self, user: User) -> None:
        if user in self._members:
            raise ValueError("User already in group")
        self._members.append(user)

    def add_expense(self, expense: Expense) -> None:
        self._expenses.append(expense)

    @property
    def members(self) -> List[User]:
        return list(self._members)

    @property
    def expenses(self) -> List[Expense]:
        return list(self._expenses)
