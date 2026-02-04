from app.domain.entities.expense import Expense
from app.domain.split_strategies.percentage import PercentageSplitStrategy


def test_percentage_split(user_a, user_b):
    strategy = PercentageSplitStrategy({
        user_a: 60,
        user_b: 40
    })

    expense = Expense(
        expense_id=1,
        paid_by=user_a,
        amount=1000,
        participants=[user_a, user_b],
        split_strategy=strategy
    )

    result = expense.split()

    assert result[user_a] == 600
    assert result[user_b] == 400
