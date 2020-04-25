from typing import Optional

from data.db_connection import DBConnection
from model.model import App, Entry

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
        # self.cursor.execute("SELECT create_app('{}','{}');".format(app_id, description))
        #self.cursor.execute("SELECT create_app(%s, %s);", (app_id, description))

        with self.conn as conn:
            conn.execute(
                text("SELECT create_app(:id, :desc)"),
                id=app_id, desc=description
            )

    def delete_app(self, app_id: str):
        # self.cursor.execute("SELECT remove_app('{}');".format(app_id))
        #self.cursor.execute("SELECT remove_app(%s);", (app_id,))

        with self.conn as conn:
            conn.execute(
                text("SELECT remove_app(:id)"),
                id=app_id
            )

    def exists(self, app_id: str) -> bool:
        return app_id in self.get_apps()

    def get_apps(self) -> list:
        """

        :return: List of dms objects
        """

        with self.conn as conn:
            db_apps = conn.execute(
                text("SELECT * FROM get_apps()")
            ).fetchall()
            return list(map(lambda x: App.from_tuple(x), db_apps))



    def get_app(self, app_id: str) -> Optional[App]:
        # self.cursor.execute("SELECT get_app('{}');".format(app_id))
        #self.cursor.execute("SELECT * FROM get_app(%s);", (app_id,))
        with self.conn as conn:
            data = conn.execute(
                text("SELECT * FROM get_app(:id)"),
                id=app_id
            ).fetchone()

            if not data:
                return None
            else:
                return App.from_tuple(data)

    def get_app_entries_limit_number(self, app_id: str, limit: int) -> []:
        #self.cursor.execute("SELECT * FROM get_app_entries_with_number_limit(%s, %s);", (app_id, limit))
        with self.conn as conn:
            db_entries = conn.execute(
                text("SELECT * FROM get_app_entries_with_number_limit(:id, :limit)"),
                id=app_id, limit=limit
            ).fetchall()
            return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def get_app_entries_limit_time(self, app_id: str, limit_min: int) -> []:
        #self.cursor.execute("SELECT * FROM get_app_entries_with_time_limit(%s, %s);", (app_id, limit_min))
        with self.conn as conn:
            db_entries = conn.execute(
                text("SELECT * FROM get_app_entries_with_time_limit(:id, :limit_min)"),
                id=app_id, limit=limit_min
            ).fetchall()
            return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def get_all_app_entries(self, app_id: str) -> []:
        #self.cursor.execute("SELECT * FROM get_all_app_entries(%s);", (app_id,))
        with self.conn as conn:
            db_entries = conn.execute(
                text("SELECT * FROM get_all_app_entries(:id)"),
                id=app_id
            ).fetchall()
            return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def add_app_entry(self, app_id: str, data: str):
        # self.cursor.execute("SELECT add_app_entry('{}', '{}');".format(app_id, data))
        #self.cursor.execute("SELECT add_app_entry(%s, %s);", (app_id, data))

        with self.conn as conn:
            conn.execute(
                text("SELECT add_app_entry(:id, :data)"),
                id=app_id, data=data
            )
