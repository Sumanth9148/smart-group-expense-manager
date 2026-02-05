"""Tests for custom split strategy."""

from app.domain.entities.expense import Expense
from app.domain.split_strategies.custom import CustomSplitStrategy


def test_custom_split(user_a, user_b):
    """Verify custom split returns assigned amounts."""
    strategy = CustomSplitStrategy({
        user_a: 700,
        user_b: 300
    })

    expense = Expense(
        expense_id=1,
        paid_by=user_a,
        amount=1000,
        participants=[user_a, user_b],
        split_strategy=strategy
    )

    result = expense.split()

    assert result[user_a] == 700
    assert result[user_b] == 300
