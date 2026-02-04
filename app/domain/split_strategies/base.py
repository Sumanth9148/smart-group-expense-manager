from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.expense import Expense
    from app.domain.entities.user import User


class SplitStrategy(ABC):
    @abstractmethod
    def split(self, expense: "Expense") -> Dict["User", float]:
        pass


