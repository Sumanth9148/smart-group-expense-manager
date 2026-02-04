from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from .db import MySQLDatabase


class UserRepositoryMySQL(UserRepository):

    def __init__(self, db: MySQLDatabase):
        self._db = db

    def save(self, user: User) -> User:
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
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email FROM users WHERE email = %s",
            (email,)
        )

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        return User(int(row[0]), row[1], row[2])

    def get_all(self) -> list:
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
