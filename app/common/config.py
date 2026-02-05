"""App configuration helpers."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    """Simple container for DB settings."""
    host: str
    user: str
    password: str
    name: str


def load_database_config() -> DatabaseConfig:
    """Load DB settings from environment variables."""
    return DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        name=os.getenv("DB_NAME", "expense_manager"),
    )
