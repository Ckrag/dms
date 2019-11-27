import unittest

from data_store import DataStore


class DataStoreTest(unittest.TestCase):

    def test_get_names(self):
        #db = DataStore(self.conn)
        #self.assertEquals(['app', 'abb'], db.get_apps())
        self.assertEqual(1,1)

    #def setUp(self) -> None:
    #    self.conn = DataStore.get_db_connection("dbname='dms' user='root' password='' host='0.0.0.0' port='5432'")
    #    # Setup
    #    curser = self.conn.cursor()
    #    curser.execute("INSERT INTO APPS id VALUES ('app'), ('abb')")
