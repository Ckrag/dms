import unittest
from model.dms import DMS as DMS_APPLICATION


class DBTest(unittest.TestCase):

    def __init__(self, conn_str: str):
        super().__init__()
        self.conn_str = conn_str

    def runTest(self):
        test_methods = [method_name for method_name in dir(self)
                        if method_name.startswith('test') and callable(getattr(self, method_name))]
        for method in test_methods:
            getattr(self, method)()

    def test_receive_data(self):
        app_name = "my_app"
        app_entry = "my_app_entry"

        dms = DMS_APPLICATION(self.conn_str)

        accept_type = dms._JSON

        self.assertEqual(len(dms.on_apps_requested()), 2)  # '[]'

        self.assertEqual(dms.on_app_requested(app_name), 404)

        self.assertEqual(200, dms.on_data_received(app_name, app_entry, accept_type))

        self.assertTrue(len(dms.on_apps_requested()) > 2)

        self.assertTrue(len(dms.on_all_entries_requested(app_name)) > 2)

        self.assertNotEqual(dms.on_app_requested(app_name), 404)

        dms.on_app_delete(app_name)  # Uppercase to test we don't differ on case

        self.assertEqual(len(dms.on_apps_requested()), 2)

        self.assertEqual(len(dms.on_all_entries_requested(app_name)), 2)

        self.assertEqual(dms.on_app_requested(app_name), 404)
