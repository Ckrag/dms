from sqlalchemy import create_engine
from sqlalchemy.engine import Connection


class DBConnection:

    def __init__(self, config: str):
        self.engine = create_engine(config)
        self.active_conn = None

    def __enter__(self) -> Connection:
        self.active_conn = self.engine.connect()
        return self.active_conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active_conn.close()
