from uuid import UUID
from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from .db import MySQLDatabase


class UserRepositoryMySQL(UserRepository):

    def __init__(self, db: MySQLDatabase):
        self._db = db

    def save(self, user: User) -> None:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (id, name) VALUES (%s, %s)",
            (str(user.id), user.name)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name FROM users WHERE id = %s",
            (str(user_id),)
        )

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        return User(UUID(row[0]), row[1])
