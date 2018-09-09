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
        # self.cursor.execute("SELECT create_app('{}','{}');".format(app_id, description))
        self.cursor.execute("SELECT create_app(%s, %s);", (app_id, description))

    def delete_app(self, app_id: str):
        # self.cursor.execute("SELECT remove_app('{}');".format(app_id))
        self.cursor.execute("SELECT remove_app(%s);", (app_id,))

    def exists(self, app_id: str) -> bool:
        return app_id in self.get_apps()

    def get_apps(self):
        """

        :return: List of dms objects
        """
        self.cursor.execute("SELECT * FROM get_apps();")

        db_apps = self.cursor.fetchall()

        return list(map(lambda x: App.from_tuple(x), db_apps))

    def get_app(self, app_id: str) -> Optional[App]:
        # self.cursor.execute("SELECT get_app('{}');".format(app_id))
        self.cursor.execute("SELECT * FROM get_app(%s);", (app_id,))

        data = self.cursor.fetchone()

        if not data:
            return None
        else:
            return App.from_tuple(data)

    def get_app_entries(self, app_id: str) -> []:
        #self.cursor.execute("SELECT get_app_entries('{}');".format(app_id))
        self.cursor.execute("SELECT * FROM get_app_entries(%s);", (app_id,))
        db_entries = self.cursor.fetchall()
        return list(map(lambda x: Entry.from_tuple(x), db_entries))

    def add_app_entry(self, app_id: str, data: str):
        # self.cursor.execute("SELECT add_app_entry('{}', '{}');".format(app_id, data))
        self.cursor.execute("SELECT add_app_entry(%s, %s);", (app_id, data))
