from abc import ABC, abstractmethod
from typing import List
from ..entities.expense import Expense


class ExpenseRepository(ABC):

    @abstractmethod
    def save(self, expense: Expense, group_id: int) -> Expense:
        pass

    @abstractmethod
    def get_by_group(self, group_id: int) -> List[Expense]:
        pass
