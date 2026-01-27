from uuid import UUID
from typing import Optional, List
from app.domain.entities.group import Group
from app.domain.repositories.group_repository import GroupRepository
from .db import MySQLDatabase


class GroupRepositoryMySQL(GroupRepository):

    def __init__(self, db: MySQLDatabase):
        self._db = db

    def save(self, group: Group) -> None:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO expense_groups (id, name) VALUES (%s, %s)",
            (str(group.id), group.name)
        )

        for member in group.members:
            cursor.execute(
                "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
                (str(group.id), str(member.id))
            )

        conn.commit()
        cursor.close()
        conn.close()

    def get_by_id(self, group_id: UUID) -> Optional[Group]:
        """
        Minimal rehydration:
        - group id
        - group name
        (members & expenses will be added later)
        """
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name FROM expense_groups WHERE id = %s",
            (str(group_id),)
        )

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if not row:
            return None

        return Group(group_id=UUID(row[0]), name=row[1])

    def get_all(self) -> List[Group]:
        """
        Used by background tasks.
        Read-only, lightweight.
        """
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM expense_groups")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            Group(group_id=UUID(row[0]), name=row[1])
            for row in rows
        ]

