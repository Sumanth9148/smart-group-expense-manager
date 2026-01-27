from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.domain.entities.expense import Expense


class SplitStrategy(ABC):
    @abstractmethod
    def split(self, expense: "Expense") -> Dict[UUID, float]:
        pass


