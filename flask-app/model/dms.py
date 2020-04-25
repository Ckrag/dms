import json

from data.data_store import DataStore


class DMS:
    # TODO: Move to own script

    _TEXT = "Text"
    _JSON = "application/json"
    _BINARY = "multipart/form-data "

    # def __init__(self, db_connect_str: str = "dbname='dms' user='root' password='root' host='flask_db' port='5432'"):
    def __init__(self, db_connect_str: str = "postgresql://flask_db:5432/dms?user=root&password=root"):
        self._db_conn_str = db_connect_str

    def on_data_received(self, app_id: str, payload: str, accept_type: str) -> int:

        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
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
        apps = list(map(lambda x: x.json(), db.get_apps()))
        return json.dumps(apps)

    def on_app_requested(self, app_id) -> str or int:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        app = db.get_app(app_id)
        if app:
            return json.dumps(app.json())
        else:
            return 404

    def on_all_entries_requested(self, app_id: str) -> str:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        return json.dumps(list(map(lambda x: x.json(), db.get_all_app_entries(app_id))))

    def on_entries_requested_limit_number(self, app_id: str, limit: int) -> str:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        return json.dumps(list(map(lambda x: x.json(), db.get_app_entries_limit_number(app_id, limit))))

    def on_entries_requested_limit_min(self, app_id: str, limit_min: int) -> str:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        return json.dumps(list(map(lambda x: x.json(), db.get_app_entries_limit_time(app_id, limit_min))))

    def on_app_delete(self, app_id: str) -> int:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        db.delete_app(app_id)
        return 204
