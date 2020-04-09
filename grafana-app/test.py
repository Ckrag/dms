#!/usr/bin/env python3
import datetime
import sys
import unittest

from db_connection import DBConnection
from repository import data_store


class Test(unittest.TestCase):

    def test_sql_datetime_from_unix(self):
        self.assertEqual('1990-02-27 00:00:00', self.data_store._sql_time_from_unix(636076800))

    def test_get_names(self):
        apps = self.data_store.get_app_names()
        self.assertEqual(['the app', 'the other app'], apps)
        self.assertTrue(self.data_store.get_app_names())

    def test_get_app_data(self):
        entries = self.data_store.get_app_data('the app')
        self.assertEqual(1, len(entries))
        self.assertEqual([('the app', datetime.datetime(1970, 1, 1, 0, 0, 2), 'fu')], entries)

    def test_get_app_data_interval(self):
        with self.conn as conn:
            conn.execute("insert into apps (id, description) values ('interval app', 'desc of test app')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1990-02-27 00:00:00', '1')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1991-02-27 00:00:00', '2')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1992-02-27 00:00:00', '2')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1993-02-27 00:00:00', '3')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1994-02-27 00:00:00', '4')")
        self.data_store.get_app_data('interval app', )

    def tearDown(self) -> None:
        with self.conn as conn:
            conn.execute("DELETE FROM app_data")
            conn.execute("DELETE FROM apps")

    def setUp(self) -> None:
        with self.conn as conn:
            conn.execute("insert into apps (id, description) values ('the app', 'desc of test app')")
            conn.execute("insert into apps (id, description) values ('the other app', 'desc of the other app')")
            conn.execute("insert into app_data (app_id, created, txt) values ('the app', '1970-01-01 00:00:02', 'fu')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('the other app', '1970-01-01 00:00:01','bar')")

    @classmethod
    def setUpClass(cls) -> None:
        cls.conn = DBConnection(conn_str)
        cls.data_store = data_store.DataStore(cls.conn)


if __name__ == '__main__':
    conn_str = sys.argv.pop()  # Hacky, but prefer being able to dynamically parse the conn string for DB tests
    unittest.main()
