import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    user: str
    password: str
    name: str


def load_database_config() -> DatabaseConfig:
    """
    Loads database configuration from environment variables.
    Works for both local runs and Docker.
    """
    return DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        name=os.getenv("DB_NAME", "expense_manager"),
    )
