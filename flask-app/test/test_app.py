import unittest
from test import db
from model.dms import DMS as DMS_APPLICATION

# http://flask.pocoo.org/docs/1.0/testing/
# How do we mock progress in a meaningful way? (We want to test with the database too) --or do we just mock the
# data_store with an underlying sqllite3? (I guess, but so much non-production work :/)
"""
@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_apps(client):

    rv = client.get('/apps')
    print(rv)

    assert "lol" in rv.data
"""


class DBTest(unittest.TestCase):

    def test_receive_data(self):
        app_name = "my_app"
        app_entry = "my_app_entry"

        dms = DMS_APPLICATION(db.get_db_test_connect_string())

        accept_type = dms._JSON

        self.assertTrue(len(dms.on_apps_requested()) == 2)  # '[]'

        self.assertEqual(200, dms.on_data_received(app_name, app_entry, accept_type))

        self.assertTrue(len(dms.on_apps_requested()) > 2)

        self.assertTrue(len(dms.on_entries_requested(app_name)) > 2)

        dms.on_app_delete(app_name)

        self.assertTrue(len(dms.on_apps_requested()) == 2)

        self.assertTrue(len(dms.on_entries_requested(app_name)) == 2)
