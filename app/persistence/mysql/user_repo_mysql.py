"""MySQL implementation for user repository."""

from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from .db import MySQLDatabase


class UserRepositoryMySQL(UserRepository):
    """Handles user persistence in MySQL."""

    def __init__(self, db: MySQLDatabase):
        """Create repo with DB helper."""
        self._db = db

    def save(self, user: User) -> User:
        """Insert a user and return the saved record."""
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (user.name, user.email)
        )

        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return User(id=new_id, name=user.name, email=user.email)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by id."""
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email FROM users WHERE id = %s",
            (user_id,)
        )

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        return User(int(row[0]), row[1], row[2])

    def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email."""
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email FROM users WHERE LOWER(email) = LOWER(%s)",
            (email,)
        )

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        return User(int(row[0]), row[1], row[2])

    def get_all(self) -> list:
        """Return all users."""
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        )

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        users = []
        for row in rows:
            users.append(User(int(row[0]), row[1], row[2]))

        return users
