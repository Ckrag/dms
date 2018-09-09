from data.data_store import DataStore
import json


class DMS:

    # TODO: Move to own script

    _JSON = "application/json"
    _BINARY = "multipart/form-data "

    def __init__(self, db_connect_str: str = "dbname='dms' user='root' password='root' host='postgres' port='5432'"):
        self._db_conn_str = db_connect_str

    def on_data_received(self, app_id: str, payload: str, accept_type: str) -> int:

        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        with db:
            app_obj = db.get_app(app_id)
            entry_data = payload
            if not entry_data:
                return 400

            if not app_obj:
                db.create_app(app_id)

            if accept_type == self._JSON:
                db.add_app_entry(app_id, entry_data)
                return 200
            elif accept_type== self._BINARY:
                return 501
            else:
                return 400

    def on_apps_requested(self) -> str:
        db = DataStore(DataStore.get_db_connection(self._db_conn_str))
        with db:
            apps = list(map(lambda x: x.json(), db.get_apps()))
            return json.dumps(apps)
