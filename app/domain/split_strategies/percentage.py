import math
from typing import Dict
from .base import SplitStrategy
from ..entities.user import User
from ..entities.expense import Expense


class PercentageSplitStrategy(SplitStrategy):

    def __init__(self, percentages: Dict[User, float]):
        total = sum(percentages.values())
        if not math.isclose(total, 100, rel_tol=0.0, abs_tol=0.01):
            raise ValueError("Percentages must sum to 100")
        self._percentages = percentages

    def split(self, expense: Expense) -> Dict[User, float]:
        return {
            user: (expense.amount * percent / 100)
            for user, percent in self._percentages.items()
        }
