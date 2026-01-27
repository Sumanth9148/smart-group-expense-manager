import asyncio
import logging

from app.common.logger import setup_logging

from app.bootstrap.container import build_services
from app.common.background_tasks import periodic_balance_logger
from app.interface.commands import (
    user_commands,
    group_commands,
    expense_commands,
    settlement_commands
)


async def main_async():
    logging.basicConfig(level=logging.INFO)

    services = build_services()

    asyncio.create_task(
        periodic_balance_logger(
            settlement_service=services["settlement"],
            group_repository=services["group_repo"],  # exposed from container
            interval_seconds=30
        )
    )

    import argparse
    parser = argparse.ArgumentParser("Smart Group Expense Manager")
    subparsers = parser.add_subparsers()

    user_commands.register(subparsers)
    group_commands.register(subparsers)
    expense_commands.register(subparsers)
    settlement_commands.register(subparsers)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return

    args.func(args)



def main():
    setup_logging()
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

