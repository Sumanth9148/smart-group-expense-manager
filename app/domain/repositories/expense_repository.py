from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from ..entities.expense import Expense


class ExpenseRepository(ABC):

    @abstractmethod
    def save(self, expense: Expense, group_id: UUID) -> None:
        pass

    @abstractmethod
    def get_by_group(self, group_id: UUID) -> List[Expense]:
        pass
