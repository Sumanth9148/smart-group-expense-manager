from uuid import uuid4, UUID
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
import logging
logger = logging.getLogger(__name__)



class UserService:

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def create_user(self, name: str) -> User:
        user = User(id=uuid4(), name=name)
        self._user_repository.save(user)
        logger.info("Creating user")
        return user

    def get_user(self, user_id: UUID) -> User | None:
        return self._user_repository.get_by_id(user_id)
