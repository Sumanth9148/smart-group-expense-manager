from uuid import UUID
from typing import List
from app.domain.entities.expense import Expense
from app.domain.repositories.expense_repository import ExpenseRepository
from .db import MySQLDatabase


class ExpenseRepositoryMySQL(ExpenseRepository):

    def __init__(self, db: MySQLDatabase):
        self._db = db

    def save(self, expense: Expense, group_id: UUID) -> None:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (id, group_id, paid_by, amount, split_type)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                str(expense.id),
                str(group_id),
                str(expense.paid_by.id),
                expense.amount,
                expense.split_strategy.__class__.__name__
            )
        )

        for user, value in expense.split().items():
            cursor.execute(
                """
                INSERT INTO expense_splits (expense_id, user_id, amount)
                VALUES (%s, %s, %s)
                """,
                (str(expense.id), str(user.id), value)
            )

        conn.commit()
        cursor.close()
        conn.close()

    def get_by_group(self, group_id: UUID) -> List[Expense]:
        # Implemented later with rehydration
        return []
