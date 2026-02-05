"""Tests for equal split strategy."""

from app.domain.entities.expense import Expense
from app.domain.split_strategies.equal import EqualSplitStrategy


def test_equal_split(user_a, user_b, user_c):
    """Verify equal split divides amount evenly."""
    expense = Expense(
        expense_id=1,
        paid_by=user_a,
        amount=300,
        participants=[user_a, user_b, user_c],
        split_strategy=EqualSplitStrategy()
    )

    result = expense.split()

    assert result[user_a] == 100
    assert result[user_b] == 100
    assert result[user_c] == 100
