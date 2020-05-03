import unittest
from os import environ

from data.data_store import DataStore
from data.db_connection import DBConnection


class BaseTest(unittest.TestCase):

    def get_db_conn(self) -> str:
        return environ['DMS_TEST_DB_STRING']

    def setUp(self) -> None:
        store = DataStore(DBConnection(self.get_db_conn()))
        for app in store.get_apps():
            store.delete_app(app.app_id)
