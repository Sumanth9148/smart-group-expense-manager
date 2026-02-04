from typing import List, Optional
from .user import User
from .expense import Expense


class Group:
    def __init__(self, group_id: Optional[int], name: str):
        self.id = group_id
        self.name = name
        self._members: List[User] = []
        self._expenses: List[Expense] = []

    def add_member(self, user: User) -> None:
        if user in self._members:
            raise ValueError("User already in group")
        self._members.append(user)

    def remove_member(self, user: User) -> None:
        for idx, member in enumerate(self._members):
            if member.id == user.id:
                del self._members[idx]
                return
        raise ValueError("User not part of this group")

    def add_expense(self, expense: Expense) -> None:
        self._expenses.append(expense)

    @property
    def members(self) -> List[User]:
        return list(self._members)

    @property
    def expenses(self) -> List[Expense]:
        return list(self._expenses)
