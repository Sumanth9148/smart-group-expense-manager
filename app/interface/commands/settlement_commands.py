from uuid import UUID
from app.bootstrap.container import build_services


def register(subparsers):
    settlement_parser = subparsers.add_parser("settlement")
    settlement_sub = settlement_parser.add_subparsers()

    balances = settlement_sub.add_parser("balances")
    balances.add_argument("--group-id", required=True)
    balances.set_defaults(func=view_balances)


def view_balances(args):
    services = build_services()
    balances = services["settlement"].get_balances(UUID(args.group_id))

    print("\nBalances:")
    for user, balance in balances.items():
        print(f"{user.name}: {balance:.2f}")
