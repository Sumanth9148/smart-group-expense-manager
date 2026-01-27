from uuid import uuid4, UUID
from typing import List, Dict
from app.domain.entities.expense import Expense
from app.domain.repositories.expense_repository import ExpenseRepository
from app.domain.repositories.group_repository import GroupRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.split_strategies.factory import (
    SplitStrategyFactory,
    SplitType
)

import logging
logger = logging.getLogger(__name__)



class ExpenseService:

    def __init__(
        self,
        expense_repository: ExpenseRepository,
        group_repository: GroupRepository,
        user_repository: UserRepository
    ):
        self._expense_repo = expense_repository
        self._group_repo = group_repository
        self._user_repo = user_repository

    def add_expense(
        self,
        group_id: UUID,
        paid_by_id: UUID,
        participant_ids: List[UUID],
        amount: float,
        split_type: SplitType,
        split_data: Dict | None = None
    ) -> Expense:

        group = self._group_repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        paid_by = self._user_repo.get_by_id(paid_by_id)
        if not paid_by:
            raise ValueError("Payer not found")

        participants = []
        for uid in participant_ids:
            user = self._user_repo.get_by_id(uid)
            if not user:
                raise ValueError(f"User {uid} not found")
            participants.append(user)

        strategy = SplitStrategyFactory.create(split_type, split_data)

        expense = Expense(
            expense_id=uuid4(),
            paid_by=paid_by,
            amount=amount,
            participants=participants,
            split_strategy=strategy
        )

        self._expense_repo.save(expense, group_id)
        logger.info(f"Adding expense | group={group_id} | amount={amount} | split={split_type}")
        return expense
