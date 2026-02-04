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

    def get_balances(self, group_id: int) -> Dict[User, float]:
        group = self._group_repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        return self._calculator.calculate_balances(group)

    def get_settlement_suggestions(self, group_id: int) -> list[tuple[User, User, float]]:
        balances = self.get_balances(group_id)

        debtors: list[tuple[User, float]] = []
        creditors: list[tuple[User, float]] = []

        for user, balance in balances.items():
            if balance < -0.01:
                debtors.append((user, -balance))  # store positive value owed
            elif balance > 0.01:
                creditors.append((user, balance))

        debtors.sort(key=lambda x: x[1], reverse=True)
        creditors.sort(key=lambda x: x[1], reverse=True)

        suggestions: list[tuple[User, User, float]] = []

        debtor_idx = 0
        creditor_idx = 0

        while debtor_idx < len(debtors) and creditor_idx < len(creditors):
            debtor, debt_amount = debtors[debtor_idx]
            creditor, credit_amount = creditors[creditor_idx]

            amount = min(debt_amount, credit_amount)
            suggestions.append((debtor, creditor, round(amount, 2)))

            debt_amount -= amount
            credit_amount -= amount

            if debt_amount <= 0.01:
                debtor_idx += 1
            else:
                debtors[debtor_idx] = (debtor, debt_amount)

            if credit_amount <= 0.01:
                creditor_idx += 1
            else:
                creditors[creditor_idx] = (creditor, credit_amount)

        return suggestions
