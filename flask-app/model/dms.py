from data.data_store import DataStore
import json


class DMS:

    # TODO: Move to own script

    _TEXT = "Text"
    _JSON = "application/json"
    _BINARY = "multipart/form-data "

    def __init__(self, db_connect_str: str = "dbname='dms' user='root' password='root' host='postgres' port='5432'"):
        self._db_conn_str = db_connect_str

    def on_data_received(self, app_id: str, payload: str, accept_type: str) -> int:

        # lowercase the ID
        app_id = app_id.lower()

        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        with db:
            app_obj = db.get_app(app_id)
            entry_data = payload
            if not entry_data:
                return 400

            if not app_obj:
                db.create_app(app_id)

            # Either its binary or its text, we don't care for anything else when it comes to storage
            if accept_type == self._BINARY:
                return 501
            else:
                db.add_app_entry(app_id, entry_data)
                return 200

    def on_apps_requested(self) -> str:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        with db:
            apps = list(map(lambda x: x.json(), db.get_apps()))
            return json.dumps(apps)

    def on_entries_requested(self, app_id: str) -> str:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        with db:
            return json.dumps(list(map(lambda x: x.json(), db.get_app_entries(app_id))))

    def on_app_delete(self, app_id: str) -> int:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        with db:
            db.delete_app(app_id)
            return 204
