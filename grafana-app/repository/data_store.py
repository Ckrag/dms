import psycopg2


class DataStore:
    """
    Cool, annotations!
    https://www.python.org/dev/peps/pep-3107/
    """

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        return self.close()

    @staticmethod
    def get_db_connection(config: str) -> psycopg2.connect:
        """

        :return: DB cursor
        """
        return psycopg2.connect(config)

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            return True
        except Exception as e:
            return False

    def get_apps(self) -> list:
        self.cursor.execute("SELECT id FROM apps")
