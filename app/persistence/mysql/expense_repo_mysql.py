from typing import List, Dict
from app.domain.entities.expense import Expense
from app.domain.entities.user import User
from app.domain.repositories.expense_repository import ExpenseRepository
from app.domain.split_strategies.custom import CustomSplitStrategy
from .db import MySQLDatabase


class ExpenseRepositoryMySQL(ExpenseRepository):

    def __init__(self, db: MySQLDatabase):
        self._db = db

    def save(self, expense: Expense, group_id: int) -> Expense:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (group_id, paid_by, amount, split_type)
            VALUES (%s, %s, %s, %s)
            """,
            (
                group_id,
                expense.paid_by.id,
                expense.amount,
                expense.split_strategy.__class__.__name__
            )
        )

        expense_id = cursor.lastrowid
        expense.id = expense_id

        for user, value in expense.split().items():
            cursor.execute(
                """
                INSERT INTO expense_splits (expense_id, user_id, amount)
                VALUES (%s, %s, %s)
                """,
                (expense_id, user.id, value)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return expense

    def get_by_group(self, group_id: int) -> List[Expense]:
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT e.id, e.paid_by, payer.name, payer.email, e.amount, e.split_type
                FROM expenses e
                JOIN users payer ON payer.id = e.paid_by
                WHERE e.group_id = %s
                ORDER BY e.id
                """,
                (group_id,)
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()

        if not rows:
            conn.close()
            return []

        user_cache: Dict[int, User] = {}
        expenses: List[Expense] = []

        for expense_id, payer_id, payer_name, payer_email, amount, split_type in rows:
            paid_by = user_cache.get(payer_id)
            if not paid_by:
                paid_by = User(int(payer_id), payer_name, payer_email)
                user_cache[payer_id] = paid_by

            participants, amounts = self._fetch_expense_splits(conn, expense_id, user_cache)
            if not participants:
                continue

            strategy = CustomSplitStrategy(amounts)
            expenses.append(
                Expense(
                    expense_id=int(expense_id),
                    paid_by=paid_by,
                    amount=float(amount),
                    participants=participants,
                    split_strategy=strategy,
                    split_type=split_type
                )
            )

        conn.close()
        return expenses

    def _fetch_expense_splits(
        self,
        conn,
        expense_id: int,
        cache: Dict[int, User]
    ) -> tuple[List[User], Dict[User, float]]:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT u.id, u.name, u.email, es.amount
                FROM expense_splits es
                JOIN users u ON u.id = es.user_id
                WHERE es.expense_id = %s
                """,
                (expense_id,)
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()

        participants: List[User] = []
        amounts: Dict[User, float] = {}

        for user_id, name, email, amount in rows:
            participant = cache.get(user_id)
            if not participant:
                participant = User(int(user_id), name, email)
                cache[user_id] = participant

            participants.append(participant)
            amounts[participant] = float(amount)

        return participants, amounts
