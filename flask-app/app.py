#!/usr/bin/python3

import json

from flask import Flask
from flask import request

from data.data_store import DataStore

app = Flask(__name__)

# https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d

_JSON = "application/json"
_BINARY = "multipart/form-data "


@app.route('/dms/<string:app_id>', methods=['POST'])
def receive_data(app_id: str) -> str:
    db = DataStore(DataStore.get_db_connection())

    app_obj = db.get_app(app_id)

    if not app_obj:
        db.create_app(app_id)

    if request.content_type == _JSON:
        pass
    elif request.content_type == _BINARY:
        pass
    else:
        pass  # TODO: Not recognized; HTTP ERROR

    db.close()
    print(request.content_type)
    return "Running: {}".format(app_id)


@app.route('/apps', methods=['GET'])
def show_apps() -> str:
    db = DataStore(DataStore.get_db_connection())
    apps = db.get_apps()
    db.close()
    return json.dumps(apps)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
