"""Expense repository interface."""
from abc import ABC, abstractmethod
from typing import List
from ..entities.expense import Expense


"""Abstract interface for expense data access."""
class ExpenseRepository(ABC):

    """Persist an expense and return the saved expense."""
    @abstractmethod
    def save(self, expense: Expense, group_id: int) -> Expense:
        pass

        """Return all expenses for a group."""
    @abstractmethod
    def get_by_group(self, group_id: int) -> List[Expense]:
        pass
