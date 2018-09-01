import unittest
import psycopg2
from db.data import Data
from app.model import App
import datetime


class DBTest(unittest.TestCase):
    # https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d

    def test_create_delete_app(self):

        database = DBTest.get_database()

        self.assertEqual([], database.get_apps())

        app_name_one = "my_first_app"
        app_name_two = "my_second_app"

        database.create_app(app_name_one, "This app is great!")

        self.assertTrue(DBTest.table_exists(database.cursor, database._table_pre() + app_name_one))

        self.assertEqual(1, len(database.get_apps()))

        self.assertEqual(
            App(app_name_one, "some description", datetime.datetime.now()).app_id,
            database.get_app(app_name_one).app_id
        )

        database.create_app(app_name_two, "This app is great!")

        self.assertEqual(2, len(database.get_apps()))

        database.delete_app(app_name_one)
        database.delete_app(app_name_two)

        self.assertEqual(0, len(database.get_apps()))

        self.assertTrue(not DBTest.table_exists(database.cursor, database._table_pre() + app_name_one))

        database.close()

    def test_create_app_and_write_data_entry(self):
        database = DBTest.get_database()
        app_name = "my_app"
        app_data = "My app data :D"
        database.create_app(app_name, "really cool app!")

        database.add_app_entry(app_name, app_data)
        self.assertEqual(1, len(database.get_app_entries(app_name)))
        self.assertEqual(app_data, database.get_app_entries(app_name)[0].data)
        database.close()

    @staticmethod
    def get_database():
        return Data(psycopg2.connect("dbname='dms' user='root' password='root' host='0.0.0.0' port='5432'"))

    @staticmethod
    def table_exists(cursor, table_name):
        cursor.execute("SELECT * FROM pg_catalog.pg_tables;")
        has_table = False
        for tuple in cursor.fetchall():
            if table_name in tuple:
                has_table = True
        return has_table


if __name__ == '__main__':
    unittest.main()
