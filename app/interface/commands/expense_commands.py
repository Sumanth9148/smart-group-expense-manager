from uuid import UUID
from app.bootstrap.container import build_services
from app.domain.split_strategies.factory import SplitType


def register(subparsers):
    expense_parser = subparsers.add_parser("expense")
    expense_sub = expense_parser.add_subparsers()

    add = expense_sub.add_parser("add")
    add.add_argument("--group-id", required=True)
    add.add_argument("--paid-by", required=True)
    add.add_argument("--amount", required=True)
    add.add_argument("--participants", required=True)
    add.add_argument("--split", required=True)
    add.add_argument("--data")
    add.set_defaults(func=add_expense)


def add_expense(args):
    services = build_services()

    participants = [UUID(uid) for uid in args.participants.split(",")]

    split_data = None
    if args.data:
        split_data = {}
        for item in args.data.split(","):
            uid, value = item.split(":")
            split_data[UUID(uid)] = float(value)

    expense = services["expense"].add_expense(
        group_id=UUID(args.group_id),
        paid_by_id=UUID(args.paid_by),
        participant_ids=participants,
        amount=float(args.amount),
        split_type=SplitType(args.split),
        split_data=split_data
    )

    print(f"Expense added: {expense.id}")
