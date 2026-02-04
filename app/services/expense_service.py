from typing import List, Dict, Any
from app.domain.entities.expense import Expense
from app.domain.entities.user import User
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
        group_id: int,
        paid_by_id: int,
        participant_ids: List[int],
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

        normalized_split_data = None
        if split_data:
            normalized_split_data = self._normalize_split_data(split_data, participants)

        strategy = SplitStrategyFactory.create(split_type, normalized_split_data)

        expense = Expense(
            expense_id=None,
            paid_by=paid_by,
            amount=amount,
            participants=participants,
            split_strategy=strategy
        )

        saved = self._expense_repo.save(expense, group_id)
        logger.info(f"Adding expense | group={group_id} | amount={amount} | split={split_type.value}")  
        return saved

    def list_expenses(self, group_id: int) -> List[Expense]:
        group = self._group_repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        return self._expense_repo.get_by_group(group_id)

    def _normalize_split_data(
        self,
        split_data: Dict[Any, float],
        participants: List[User]
    ) -> Dict[User, float]:
        participants_index = {user.id: user for user in participants}
        normalized: Dict[User, float] = {}

        for identifier, value in split_data.items():
            if isinstance(identifier, User):
                participant = identifier
            else:
                participant_id = int(identifier)

                participant = participants_index.get(participant_id)
                if not participant:
                    raise ValueError(
                        f"Split data references unknown participant: {identifier}"
                    )

            normalized[participant] = float(value)

        return normalized
