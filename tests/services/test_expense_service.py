from unittest.mock import Mock
from app.services.expense_service import ExpenseService
from app.domain.entities.group import Group
from app.domain.entities.user import User
from app.domain.split_strategies.factory import SplitType


def test_add_expense_equal_split():
    group_id = 1
    user = User(1, "Alice", "alice@example.com")

    group_repo = Mock()
    user_repo = Mock()
    expense_repo = Mock()

    group_repo.get_by_id.return_value = Group(group_id, "Trip")
    user_repo.get_by_id.return_value = user
    expense_repo.save.side_effect = lambda exp, gid: exp  # return same expense with assigned data

    service = ExpenseService(expense_repo, group_repo, user_repo)

    expense = service.add_expense(
        group_id=group_id,
        paid_by_id=user.id,
        participant_ids=[user.id],
        amount=100,
        split_type=SplitType.EQUAL
    )

    expense_repo.save.assert_called_once()
    assert expense.amount == 100
