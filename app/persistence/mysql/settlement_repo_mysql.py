"""MySQL implementation for settlement repository."""

from typing import List
from datetime import date
from app.domain.entities.settlement import Settlement
from app.domain.entities.user import User
from app.domain.repositories.settlement_repository import SettlementRepository
from .db import MySQLDatabase


class SettlementRepositoryMySQL(SettlementRepository):
    """Handles settlement persistence in MySQL."""

    def __init__(self, db: MySQLDatabase):
        """Create repo with DB helper."""
        self._db = db

    def save(self, settlement: Settlement) -> Settlement:
        """Insert a settlement payment record."""
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO settlements (group_id, debtor_id, creditor_id, amount, settlement_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                settlement.group_id,
                settlement.debtor.id,
                settlement.creditor.id,
                settlement.amount,
                settlement.settlement_date,
            ),
        )

        settlement.id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        return settlement

    def get_by_group(self, group_id: int) -> List[Settlement]:
        """Get all settlements for a group."""
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT s.id, s.group_id, s.debtor_id, d.name, d.email,
                       s.creditor_id, c.name, c.email, s.amount, s.settlement_date
                FROM settlements s
                JOIN users d ON d.id = s.debtor_id
                JOIN users c ON c.id = s.creditor_id
                WHERE s.group_id = %s
                ORDER BY s.settlement_date DESC
                """,
                (group_id,),
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        if not rows:
            return []

        settlements = []
        for row in rows:
            debtor = User(row[2], row[3], row[4])
            creditor = User(row[5], row[6], row[7])
            settlement = Settlement(
                settlement_id=row[0],
                group_id=row[1],
                debtor=debtor,
                creditor=creditor,
                amount=float(row[8]),
                settlement_date=row[9],
            )
            settlements.append(settlement)

        return settlements

    def get_all(self) -> List[Settlement]:
        """Get all settlements."""
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT s.id, s.group_id, s.debtor_id, d.name, d.email,
                       s.creditor_id, c.name, c.email, s.amount, s.settlement_date
                FROM settlements s
                JOIN users d ON d.id = s.debtor_id
                JOIN users c ON c.id = s.creditor_id
                ORDER BY s.settlement_date DESC
                """
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

        if not rows:
            return []

        settlements = []
        for row in rows:
            debtor = User(row[2], row[3], row[4])
            creditor = User(row[5], row[6], row[7])
            settlement = Settlement(
                settlement_id=row[0],
                group_id=row[1],
                debtor=debtor,
                creditor=creditor,
                amount=float(row[8]),
                settlement_date=row[9],
            )
            settlements.append(settlement)

        return settlements
