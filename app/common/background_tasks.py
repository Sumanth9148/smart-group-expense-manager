import asyncio
import logging
from app.services.settlement_service import SettlementService
from app.domain.repositories.group_repository import GroupRepository


async def periodic_balance_logger(
    settlement_service: SettlementService,
    group_repository: GroupRepository,
    interval_seconds: int = 30
) -> None:
    """
    Periodically recompute balances for all groups
    and log a short summary.
    """
    logging.info("Background balance logger started")

    while True:
        try:
            groups = group_repository.get_all()

            for group in groups:
                balances = settlement_service.get_balances(group.id)

                summary = ", ".join(
                    f"{user.name}: {balance:.2f}"
                    for user, balance in balances.items()
                )

                logging.info(
                    f"[Group: {group.name} | {group.id}] Balances → {summary}"
                )

        except Exception as exc:
            logging.exception("Error while recomputing balances", exc_info=exc)

        await asyncio.sleep(interval_seconds)
