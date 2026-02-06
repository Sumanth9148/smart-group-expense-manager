"""Tests for settlement calculator."""

from app.domain.entities.group import Group
from app.domain.entities.expense import Expense
from app.domain.domain_services.settlement_calculator import SettlementCalculator
from app.domain.split_strategies.equal import EqualSplitStrategy


def test_settlement_calculation(user_a, user_b):
    """Verify balances after one equal split expense."""
    group = Group(group_id=1, name="goa")

    group.add_member(user_a)
    group.add_member(user_b)

    expense = Expense(
        expense_id=1,
        paid_by=user_a,
        amount=100,
        participants=[user_a, user_b],
        split_strategy=EqualSplitStrategy()
    )

    group.add_expense(expense)

    calculator = SettlementCalculator()
    balances = calculator.calculate_balances(group)

    assert balances[user_a] == 50
    assert balances[user_b] == -50
