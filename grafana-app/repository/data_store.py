import time
from datetime import datetime

from db_connection import DBConnection

from sqlalchemy.sql import text


class DataStore:
    """
    Cool, annotations!
    https://www.python.org/dev/peps/pep-3107/
    """

    def __init__(self, conn: DBConnection):
        self.connection = conn

    def get_app_names(self) -> list:
        with self.connection as conn:
            res_proxy = conn.execute("SELECT id FROM apps")
            return [list(row)[0] for row in res_proxy]

    def get_data_series_var(self, app_id: str)-> str:
        with self.connection as conn:
            return conn.execute(
                text("SELECT data_series_var FROM app_config WHERE app_id=:app_id"),
                app_id=app_id
            ).fetchone()[0]

    def get_app_data(self, app_id: str, interval_start_unix: int = 0, interval_end_unix: int = time.time()):
        start = self._sql_time_from_unix(interval_start_unix)
        end = self._sql_time_from_unix(interval_end_unix)

        with self.connection as conn:
            res_proxy = conn.execute(
                text("SELECT * FROM app_data WHERE app_id=:id and created >= :start and created <= :end"),
                id=app_id, start=start, end=end
            ).fetchall()
            return [list(row) for row in res_proxy]

    def _sql_time_from_unix(self, unix: int) -> str:
        return datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
