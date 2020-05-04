from model.dms import DMS as DMS_APPLICATION
from test.base_test import BaseTest


class DBTest(BaseTest):

    def test_receive_data(self):
        app_name = "my_app"
        app_entry = "my_app_entry"

        dms = DMS_APPLICATION(self.get_db_conn())

        accept_type = dms._JSON

        self.assertEqual(dms.on_apps_requested(), '[]')

        self.assertEqual(dms.on_app_requested(app_name), 404)

        self.assertEqual(400, dms.on_data_received(app_name, app_entry, accept_type, 'fubar'))

        self.assertEqual(200, dms.on_data_received(app_name, app_entry, accept_type), 123)

        self.assertEqual(len(dms.on_apps_requested()), 78)

        self.assertTrue(len(dms.on_all_entries_requested(app_name)), 78)

        self.assertNotEqual(dms.on_app_requested(app_name), 404)

        dms.on_app_delete(app_name)  # Uppercase to test we don't differ on case

        self.assertEqual(len(dms.on_apps_requested()), 2)

        self.assertEqual(len(dms.on_all_entries_requested(app_name)), 2)

        self.assertEqual(dms.on_app_requested(app_name), 404)
