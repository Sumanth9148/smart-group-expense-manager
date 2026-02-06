"""Settlement/Payment entity to track paid settlements."""

from typing import Optional
from datetime import date
from app.domain.entities.user import User


class Settlement:
    """Represents a settlement payment between two users."""

    def __init__(
        self,
        settlement_id: Optional[int],
        group_id: int,
        debtor: User,
        creditor: User,
        amount: float,
        settlement_date: Optional[date] = None,
    ):
        """Create a settlement record."""
        self.id = settlement_id
        self.group_id = group_id
        self.debtor = debtor
        self.creditor = creditor
        self.amount = amount
        self.settlement_date = settlement_date or date.today()

    def __repr__(self) -> str:
        return (
            f"Settlement({self.debtor.name} → {self.creditor.name}: "
            f"{self.amount:.2f} on {self.settlement_date})"
        )
