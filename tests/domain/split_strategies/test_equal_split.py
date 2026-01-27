from uuid import uuid4
from app.domain.entities.expense import Expense
from app.domain.split_strategies.equal import EqualSplitStrategy


def test_equal_split(user_a, user_b, user_c):
    expense = Expense(
        expense_id=uuid4(),
        paid_by=user_a,
        amount=300,
        participants=[user_a, user_b, user_c],
        split_strategy=EqualSplitStrategy()
    )

    result = expense.split()

    assert result[user_a] == 100
    assert result[user_b] == 100
    assert result[user_c] == 100
