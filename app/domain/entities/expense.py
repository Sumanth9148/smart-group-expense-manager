from typing import Dict
from uuid import UUID
from app.domain.split_strategies.base import SplitStrategy


class Expense:
    def __init__(
        self,
        id: UUID,
        amount: float,
        paid_by: UUID,
        participants: list[UUID],
        split_strategy: SplitStrategy
    ):
        self.id = id
        self.amount = amount
        self.paid_by = paid_by
        self.participants = participants
        self.split_strategy = split_strategy

    def split(self) -> Dict[UUID, float]:
        return self.split_strategy.split(self)

