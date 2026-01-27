from typing import Dict
from .base import SplitStrategy
from ..entities.user import User
from ..entities.expense import Expense


class CustomSplitStrategy(SplitStrategy):

    def __init__(self, amounts: Dict[User, float]):
        self._amounts = amounts

    def split(self, expense: Expense) -> Dict[User, float]:
        total_assigned = sum(self._amounts.values())

        if total_assigned != expense.amount:
            raise ValueError("Custom split amounts must match expense total")

        return self._amounts
