from uuid import uuid4
from unittest.mock import Mock
from app.services.expense_service import ExpenseService
from app.domain.entities.group import Group
from app.domain.entities.user import User
from app.domain.split_strategies.factory import SplitType


def test_add_expense_equal_split():
    group_id = uuid4()
    user = User(uuid4(), "Alice")

    group_repo = Mock()
    user_repo = Mock()
    expense_repo = Mock()

    group_repo.get_by_id.return_value = Group(group_id, "Trip")
    user_repo.get_by_id.return_value = user

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
