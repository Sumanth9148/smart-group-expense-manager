"""Pytest shared fixtures and path setup."""

import sys
from pathlib import Path
import pytest

# Ensure project root is on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.domain.entities.user import User


@pytest.fixture
def user_a():
    """Return a sample user fixture."""
    return User(id=1, name="Alice", email="alice@example.com")


# @pytest.fixture
# def user_b():
#     return User(id=2, name="Bob", email="bob@example.com")


# @pytest.fixture
# def user_c():
#     return User(id=3, name="Charlie", email="charlie@example.com")
