import datetime

from data.data_store import DBConnection
from data.data_store import DataStore
from model.model import App
from test.base_test import BaseTest


class DBTest(BaseTest):
    # https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d

    def test_create_delete_app(self):
        database = self.database

        self.assertEqual([], database.get_apps())

        app_name_one = "my_first_app"
        app_name_two = "my_second_app"

        database.create_app(app_name_one, "This dms is great!")
        self.assertTrue(database.get_apps())

        database.add_app_entry(app_name_one, "my first entry")
        self.assertTrue(database.get_all_app_entries(app_name_one))

        self.assertEqual(1, len(database.get_apps()))

        self.assertEqual(
            App(app_name_one, "some description", datetime.datetime.now()).app_id,
            database.get_app(app_name_one).app_id
        )

        database.create_app(app_name_two, "This dms is great!")

        self.assertEqual(2, len(database.get_apps()))

        database.delete_app(app_name_one)
        database.delete_app(app_name_two)

        self.assertEqual(0, len(database.get_apps()))

        self.assertFalse(database.get_all_app_entries(app_name_one))

    def test_create_app_and_write_data_entry(self):
        database = self.database
        app_name = "my_app"
        app_data = "My dms data :D"
        database.create_app(app_name, "really cool dms!")

        database.add_app_entry(app_name, app_data)
        self.assertEqual(1, len(database.get_all_app_entries(app_name)))
        self.assertEqual(app_data, database.get_all_app_entries(app_name)[0].data)

    def test_get_all_app_entries(self):
        self.database.create_app('app')
        self.database.add_app_entry('add', '1')
        self.database.add_app_entry('add', '2')
        self.database.add_app_entry('add', '3')
        entries = self.database.get_all_app_entries('app')
        self.assertEqual(len(entries), 3)

    def test_get_app_entries_limit_number(self):
        self.database.create_app('app')
        self.database.add_app_entry('app', '1')
        self.database.add_app_entry('app', '2')
        self.database.add_app_entry('app', '3')
        entries = self.database.get_app_entries_limit_number('app', 2)
        self.assertEqual(len(entries), 2)

    def test_get_app_entries_limit_time(self):
        self.database.create_app('app')
        self.database.add_app_entry('app', '1', datetime.datetime(1, 1, 1))
        self.database.add_app_entry('app', '2', datetime.datetime(1, 1, 1))
        self.database.add_app_entry('app', '3')
        entries = self.database.get_app_entries_limit_time('app', 1)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].data, '1')

    def setUp(self) -> None:
        super().setUp()
        self.database = DataStore(DBConnection(self.get_db_conn()))
