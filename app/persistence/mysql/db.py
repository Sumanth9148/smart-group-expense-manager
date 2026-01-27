import time
import mysql.connector  # type: ignore
from mysql.connector import Error  # type: ignore  


class MySQLDatabase:

    def __init__(self, config):
        self._config = config

    def connect(self):
        retries = 10
        delay = 2

        for attempt in range(retries):
            try:
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



