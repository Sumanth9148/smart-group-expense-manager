"""Settlement service for balances and suggestions."""

from typing import Dict
from datetime import date
from app.domain.domain_services.settlement_calculator import SettlementCalculator
from app.domain.entities.user import User
from app.domain.entities.settlement import Settlement
from app.domain.repositories.group_repository import GroupRepository
from app.domain.repositories.settlement_repository import SettlementRepository


class SettlementService:
    """Handles balance calculation and settlement suggestions."""

    def __init__(
        self,
        group_repository: GroupRepository,
        calculator: SettlementCalculator,
        settlement_repository: SettlementRepository = None
    ):
        """Create the service with repo and calculator."""
        self._group_repo = group_repository
        self._calculator = calculator
        self._settlement_repo = settlement_repository

    def get_balances(self, group_id: int) -> Dict[User, float]:
        """Return net balances for a group after deducting recorded settlements."""
        group = self._group_repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        balances = self._calculator.calculate_balances(group)
        
        # Deduct recorded settlements from balances
        if self._settlement_repo:
            settlements = self._settlement_repo.get_by_group(group_id)
            
            # Convert balances to dict keyed by user ID for easier lookup
            balance_by_id = {user.id: balance for user, balance in balances.items()}
            user_by_id = {user.id: user for user in balances.keys()}
            
            for settlement in settlements:
                # Debtor's balance improves (becomes less negative/more positive)
                if settlement.debtor.id in balance_by_id:
                    balance_by_id[settlement.debtor.id] += float(settlement.amount)
                    
                # Creditor's balance decreases (becomes less positive/more negative)
                if settlement.creditor.id in balance_by_id:
                    balance_by_id[settlement.creditor.id] -= float(settlement.amount)
            
            # Reconstruct balances dict with User objects
            balances = {user_by_id[user_id]: balance for user_id, balance in balance_by_id.items()}
        
        # Normalize near-zero balances
        normalized: Dict[User, float] = {}
        for user, balance in balances.items():
            if abs(balance) < 0.01:
                normalized[user] = 0.0
            else:
                normalized[user] = round(balance, 2)
        
        return normalized

    def get_settlement_suggestions(self, group_id: int) -> list[tuple[User, User, float]]:
        """Return payment suggestions to settle balances."""
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

    def get_balances_after_settlement(self, group_id: int) -> Dict[User, float]:
        """Return balances after applying settlement suggestions (simulated)."""
        balances = self.get_balances(group_id)
        suggestions = self.get_settlement_suggestions(group_id)

        for debtor, creditor, amount in suggestions:
            balances[debtor] = balances.get(debtor, 0) + amount
            balances[creditor] = balances.get(creditor, 0) - amount

        normalized: Dict[User, float] = {}
        for user, balance in balances.items():
            if abs(balance) < 0.01:
                normalized[user] = 0.0
            else:
                normalized[user] = round(balance, 2)

        return normalized

    def record_settlement(
        self, group_id: int, debtor_id: int, creditor_id: int, amount: float
    ) -> Settlement:
        """Record a settlement payment in the database."""
        if not self._settlement_repo:
            raise ValueError("Settlement repository not configured")

        # Get user details
        group = self._group_repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        debtor = None
        creditor = None

        for member in group.members:
            if member.id == debtor_id:
                debtor = member
            if member.id == creditor_id:
                creditor = member

        if not debtor or not creditor:
            raise ValueError("One or both users not found in group")

        settlement = Settlement(
            settlement_id=None,
            group_id=group_id,
            debtor=debtor,
            creditor=creditor,
            amount=amount,
            settlement_date=date.today(),
        )

        return self._settlement_repo.save(settlement)

    def get_all_settlements(self, group_id: int) -> list[Settlement]:
        """Get all recorded settlements for a group."""
        if not self._settlement_repo:
            return []

        return self._settlement_repo.get_by_group(group_id)

