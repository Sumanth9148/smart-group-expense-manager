from uuid import UUID
from typing import Dict
from app.domain.domain_services.settlement_calculator import SettlementCalculator
from app.domain.entities.user import User
from app.domain.repositories.group_repository import GroupRepository


class SettlementService:

    def __init__(
        self,
        group_repository: GroupRepository,
        calculator: SettlementCalculator
    ):
        self._group_repo = group_repository
        self._calculator = calculator

    def get_balances(self, group_id: UUID) -> Dict[User, float]:
        group = self._group_repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        return self._calculator.calculate_balances(group)
