import unittest
from test import db
import datetime
from model.model import App


class DBTest(unittest.TestCase):
    # https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d

    def test_create_delete_app(self):

        database = db.get_database()

        self.assertEqual([], database.get_apps())

        app_name_one = "my_first_app"
        app_name_two = "my_second_app"

        database.create_app(app_name_one, "This dms is great!")
        self.assertTrue(database.get_apps())

        database.add_app_entry(app_name_one, "my first entry")
        self.assertTrue(database.get_app_entries(app_name_one))

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

        self.assertFalse(database.get_app_entries(app_name_one))

        database.close()

    def test_create_app_and_write_data_entry(self):
        database = db.get_database()
        app_name = "my_app"
        app_data = "My dms data :D"
        database.create_app(app_name, "really cool dms!")

        database.add_app_entry(app_name, app_data)
        self.assertEqual(1, len(database.get_app_entries(app_name)))
        self.assertEqual(app_data, database.get_app_entries(app_name)[0].data)
        database.close()


if __name__ == '__main__':
    unittest.main()
