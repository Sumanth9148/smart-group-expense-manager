import pytest
from uuid import uuid4
from app.domain.entities.user import User


@pytest.fixture
def user_a():
    return User(id=uuid4(), name="Alice")


@pytest.fixture
def user_b():
    return User(id=uuid4(), name="Bob")


@pytest.fixture
def user_c():
    return User(id=uuid4(), name="Charlie")
