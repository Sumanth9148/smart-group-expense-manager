"""Equal split strategy implementation."""

from typing import Dict
from .base import SplitStrategy
from ..entities.user import User
from ..entities.expense import Expense


class EqualSplitStrategy(SplitStrategy):
    """Split amount equally among participants."""

    def split(self, expense: Expense) -> Dict[User, float]:
        """Compute equal share for each participant."""
        if not expense.participants:
            raise ValueError("Expense must have participants")

        per_head = expense.amount / len(expense.participants)

        return {user: per_head for user in expense.participants}

