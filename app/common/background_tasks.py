import asyncio
import asyncio
import logging
from app.services.settlement_service import SettlementService
from app.domain.repositories.group_repository import GroupRepository

logger = logging.getLogger(__name__)  


async def periodic_balance_logger(
    settlement_service: SettlementService,
    group_repository: GroupRepository,
    interval_seconds: int = 30
) -> None:
    """
    Periodically recompute balances for all groups
    and log a short summary.
    """
    logger.info(f"Background balance logger started (interval={interval_seconds}s)")  

    try:
        while True:
            try:
                groups = group_repository.get_all() or []  

                for group in groups:
                    balances = settlement_service.get_balances(group.id)

                    summary = ", ".join(
                        f"{user.name}: {balance:.2f}"
                        for user, balance in balances.items()
                    ) or "no balances"  

                    logger.info(
                        f"[Group: {group.name} | {group.id}] Balances → {summary}"
                    )

            except Exception:
                logger.exception("Error while recomputing balances")  

            await asyncio.sleep(interval_seconds)
    except asyncio.CancelledError:  
        logger.info("Background balance logger stopped")
        raise
