from typing import Optional

import psycopg2

from model.model import App, Entry


class DataStore:
    """
    Cool annotations!
    https://www.python.org/dev/peps/pep-3107/
    """

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    @staticmethod
    def _table_pre() -> str:
        return "app_entries_"

    @staticmethod
    def _table_name(app_id: str) -> str:
        return DataStore._table_pre() + app_id

    @staticmethod
    def get_db_connection() -> psycopg2.connect:
        """

        :return: DB cursor
        """
        return psycopg2.connect("dbname='dms' user='root' password='root' host='postgres' port='5432'")

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            return True
        except Exception as e:
            return False

    def create_app(self, app_id: str, description=""):
        self.cursor.execute(
            "CREATE TABLE {} (txt TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP); INSERT INTO apps (id, description) VALUES ('{}', '{}');".format(
                DataStore._table_name(app_id), app_id, description))

    def delete_app(self, app_id: str):
        self.cursor.execute("DROP TABLE {};DELETE FROM apps WHERE id='{}';".format(DataStore._table_name(app_id), app_id))

    def exists(self, app_id: str) -> bool:
        return app_id in self.get_apps()

    def get_apps(self):
        """

        :return: List of dms objects
        """
        self.cursor.execute("SELECT * FROM apps;")

        db_apps = self.cursor.fetchall()

        return list(map(lambda x: App.from_tuple(x), db_apps))

    def get_app(self, app_id: str) -> Optional[App]:
        self.cursor.execute("SELECT * FROM apps WHERE id='{}';".format(app_id))

        data = self.cursor.fetchone()

        if not data:
            return None
        else:
            return App.from_tuple(data)

    def get_app_entries(self, app_id: str) -> []:
        self.cursor.execute("SELECT * FROM {};".format(DataStore._table_name(app_id)))
        db_entries = self.cursor.fetchall()
        return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def add_app_entry(self, app_id: str, data: str):
        self.cursor.execute("INSERT INTO {} (txt) VALUES ('{}');".format(DataStore._table_name(app_id), data))
