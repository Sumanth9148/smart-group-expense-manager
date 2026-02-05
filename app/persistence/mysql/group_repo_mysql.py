"""MySQL implementation for group repository."""

from typing import Optional, List, Dict
from app.domain.entities.group import Group
from app.domain.entities.user import User
from app.domain.entities.expense import Expense
from app.domain.repositories.group_repository import GroupRepository
from app.domain.split_strategies.custom import CustomSplitStrategy
from .db import MySQLDatabase


class GroupRepositoryMySQL(GroupRepository):
    """Handles group persistence in MySQL."""

    def __init__(self, db: MySQLDatabase):
        """Create repo with DB helper."""
        self._db = db

    def save(self, group: Group) -> Group:
        """Insert or update a group and its members."""
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            if group.id is None:
                cursor.execute(
                    "INSERT INTO expense_groups (name) VALUES (%s)",
                    (group.name,)
                )
                group_id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE expense_groups SET name = %s WHERE id = %s",
                    (group.name, group.id)
                )
                group_id = group.id

            cursor.execute(
                "DELETE FROM group_members WHERE group_id = %s",
                (group_id,)
            )

            members = group.members
            if members:
                cursor.executemany(
                    """
                    INSERT INTO group_members (group_id, user_id)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE user_id = VALUES(user_id)
                    """,
                    [
                        (group_id, member.id)
                        for member in members
                    ]
                )

            conn.commit()
            group.id = group_id
            return group
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, group_id: int) -> Optional[Group]:
        """Fetch a group with members and expenses."""
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, name FROM expense_groups WHERE id = %s",
                (group_id,)
            )

            row = cursor.fetchone()
            if not row:
                return None

            group = Group(group_id=int(row[0]), name=row[1])

            for member in self._fetch_members(conn, group.id):
                group.add_member(member)

            for expense in self._fetch_expenses(conn, group.id):
                group.add_expense(expense)

            return group
        finally:
            cursor.close()
            conn.close()

    def get_all(self) -> List[Group]:
        """Return all groups (read-only)."""
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM expense_groups")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            Group(group_id=int(row[0]), name=row[1])
            for row in rows
        ]

    def _fetch_members(self, conn, group_id: int) -> List[User]:
        """Load group members for a given group id."""
        cursor = conn.cursor()
        rows: List[tuple] = []
        try:
            cursor.execute(
                """
                SELECT u.id, u.name, u.email
                FROM group_members gm
                JOIN users u ON gm.user_id = u.id
                WHERE gm.group_id = %s
                """,
                (group_id,)
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()

        return [User(int(row[0]), row[1], row[2]) for row in rows]

    def _fetch_expenses(self, conn, group_id: int) -> List[Expense]:
        """Load expenses for a given group id."""
        cursor = conn.cursor()
        rows: List[tuple] = []
        try:
            cursor.execute(
                """
                SELECT e.id, e.paid_by, payer.name, payer.email, e.amount, e.split_type
                FROM expenses e
                JOIN users payer ON payer.id = e.paid_by
                WHERE e.group_id = %s
                """,
                (group_id,)
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()

        if not rows:
            return []

        user_cache: Dict[int, User] = {}
        expenses: List[Expense] = []

        for expense_id, payer_id, payer_name, payer_email, amount, split_type in rows:
            paid_by = user_cache.get(payer_id) or User(int(payer_id), payer_name, payer_email)
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

        return expenses

    def _fetch_expense_splits(
        self,
        conn,
        expense_id: int,
        cache: Dict[int, User]
    ) -> tuple[List[User], Dict[User, float]]:
        """Load participants and amounts for an expense."""
        cursor = conn.cursor()
        rows: List[tuple] = []
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
            user = cache.get(user_id)
            if not user:
                user = User(int(user_id), name, email)
                cache[user_id] = user

            participants.append(user)
            amounts[user] = float(amount)

        return participants, amounts

