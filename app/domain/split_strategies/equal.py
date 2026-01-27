from typing import Dict
from .base import SplitStrategy
from ..entities.user import User
from ..entities.expense import Expense


class EqualSplitStrategy(SplitStrategy):

    def split(self, expense: Expense) -> Dict[User, float]:
        if not expense.participants:
            raise ValueError("Expense must have participants")

        per_head = expense.amount / len(expense.participants)

        return {user: per_head for user in expense.participants}

