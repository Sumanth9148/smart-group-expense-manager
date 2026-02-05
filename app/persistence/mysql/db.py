"""MySQL connection helper with retry logic."""

import time
import mysql.connector  # type: ignore
from mysql.connector import Error  # type: ignore  


class MySQLDatabase:
    """Provides DB connections using stored config."""

    def __init__(self, config):
        """Store DB config for later connections."""
        self._config = config

    def connect(self):
        """Open a DB connection with retries."""
        retries = 10
        delay = 2

        for attempt in range(retries):
            try:
                # Attempt to connect to MySQL
                return mysql.connector.connect(
                    host=self._config.host,
                    user=self._config.user,
                    password=self._config.password,
                    database=self._config.name,
                )
            except Error:
                if attempt == retries - 1:
                    raise
                time.sleep(delay)



