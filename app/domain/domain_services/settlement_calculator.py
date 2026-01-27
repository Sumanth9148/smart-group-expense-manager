from typing import Dict
from ..entities.group import Group
from ..entities.user import User


class SettlementCalculator:

    def calculate_balances(self, group: Group) -> Dict[User, float]:
        balances: Dict[User, float] = {}

        for expense in group.expenses:
            splits = expense.split()

            for user, owed in splits.items():
                balances[user] = balances.get(user, 0) - owed

            balances[expense.paid_by] = (
                balances.get(expense.paid_by, 0) + expense.amount
            )

        return balances
