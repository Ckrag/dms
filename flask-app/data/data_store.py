from typing import Optional

from data.db_connection import DBConnection
from model.model import App, Entry
from datetime import datetime

from sqlalchemy.sql import text


class DataStore:
    """
    Cool, annotations!
    https://www.python.org/dev/peps/pep-3107/
    """

    def __init__(self, conn: DBConnection):
        self.conn = conn

    @staticmethod
    def get_db_connection(config: str) -> DBConnection:
        return DBConnection(config)

    def create_app(self, app_id: str, description=""):
        with self.conn as conn:
            conn.execute(
                text("INSERT INTO apps (id, description) VALUES (:app_id, :app_desc) ON CONFLICT(id) DO NOTHING;"),
                app_id=app_id, app_desc=description
            )
            conn.execute(
                text("INSERT INTO app_config (app_id, data_series_var) VALUES (:app_id, null) ON CONFLICT(app_id) DO NOTHING;"),
                app_id=app_id
            )

    def delete_app(self, app_id: str):
        with self.conn as conn:
            conn.execute(
                text("DELETE FROM apps WHERE id=:app_id"),
                app_id=app_id
            )

    def apply_config(self, app_id: str, config: dict):
        with self.conn as conn:
            for k, v in config.items():
                conn.execute(
                    text(f"UPDATE app_config SET {k}=:v WHERE app_id=:app_id"),
                    v=v, app_id=app_id
                )

    def get_config(self, app_id: str) -> dict:
        with self.conn as conn:
            return conn.execute(
                text("SELECT * FROM app_config WHERE app_id=:app_id"),
                app_id=app_id
            ).fetchone()

    def exists(self, app_id: str) -> bool:
        return app_id in self.get_apps()

    def get_apps(self) -> list:
        """

        :return: List of dms objects
        """

        with self.conn as conn:
            db_apps = conn.execute(
                text("SELECT * FROM apps")
            ).fetchall()
            return list(map(lambda x: App.from_tuple(x), db_apps))

    def get_app(self, app_id: str) -> Optional[App]:
        with self.conn as conn:
            data = conn.execute(
                text("SELECT * FROM apps WHERE id=:app_id"),
                app_id=app_id
            ).fetchone()

            if not data:
                return None
            else:
                return App.from_tuple(data)

    def get_app_entries_limit_number(self, app_id: str, limit: int) -> []:
        with self.conn as conn:
            db_entries = conn.execute(
                text("SELECT * FROM (SELECT * FROM app_data WHERE app_id=:app_id ORDER BY created DESC LIMIT :entries_limit) AS entries ORDER BY created ASC"),
                app_id=app_id, entries_limit=limit
            ).fetchall()
            return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def get_app_entries_limit_time(self, app_id: str, limit_min: int) -> []:
        with self.conn as conn:
            db_entries = conn.execute(
                #text("SELECT * FROM get_app_entries_with_time_limit(:id, :limit_min)"),
                text("SELECT * FROM app_data WHERE app_id=:app_id AND created > now() - INTERVAL '1 min' * :minute_limit"),
                app_id=app_id, minute_limit=limit_min
            ).fetchall()
            return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def get_all_app_entries(self, app_id: str) -> []:
        with self.conn as conn:
            db_entries = conn.execute(
                text("SELECT * FROM app_data WHERE app_id=:app_id"),
                app_id=app_id
            ).fetchall()
            return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def add_app_entry(self, app_id: str, data: str, created: datetime = None):
        with self.conn as conn:
            if created:
                conn.execute(
                    text("INSERT INTO app_data (app_id, txt, created) VALUES (:app_id, :entry_data, :created)"),
                    app_id=app_id, entry_data=data, created=created
                )
            else:
                conn.execute(
                    text("INSERT INTO app_data (app_id, txt) VALUES (:app_id, :entry_data)"),
                    app_id=app_id, entry_data=data
                )

