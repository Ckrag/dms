#!/usr/bin/env python3

import unittest

from repository import data_store


class Test(unittest.TestCase):

    def test_get_names(self):
        db = data_store.DataStore(self.conn)
        self.assertEquals(['app', 'abb'], db.get_apps())
        self.assertTrue(False)
        print("LOL")

    def setUp(self) -> None:
        self.conn = data_store.DataStore.get_db_connection(
            "dbname='dms' user='root' host='0.0.0.0' port='5432'")
        # Setup
        curser = self.conn.cursor()
        curser.execute("INSERT INTO APPS id VALUES ('app'), ('abb')")


if __name__ == '__main__':
    unittest.main()
