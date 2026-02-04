from typing import Dict, List, Optional
from datetime import date
from app.domain.entities.user import User
from app.domain.split_strategies.base import SplitStrategy

class Expense:
    def __init__(
        self,
        expense_id: Optional[int],
        paid_by: User,
        amount: float,
        participants: List[User],
        split_strategy: SplitStrategy,
        description: str = "",
        expense_date: Optional[date] = None,
        split_type: str = "",
    ):
        self.id = expense_id
        self.paid_by = paid_by
        self.amount = amount
        self.participants = participants
        self.split_strategy = split_strategy
        self.description = description
        self.expense_date = expense_date or date.today()
        self.split_type = split_type or split_strategy.__class__.__name__

    def split(self) -> Dict[User, float]:
        return self.split_strategy.split(self)

