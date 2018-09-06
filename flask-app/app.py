#!/usr/bin/python3

import json

from flask import Flask
from flask import request
from flask import abort

from data.data_store import DataStore

app = Flask(__name__)

# https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d
# http://flask.pocoo.org/docs/1.0/quickstart/#about-responses

_JSON = "application/json"
_BINARY = "multipart/form-data "


@app.route('/app/<string:app_id>', methods=['POST'])
def receive_data(app_id: str) -> str or int:
    db = DataStore(DataStore.get_db_connection())

    with db:
        app_obj = db.get_app(app_id)
        entry_data = request.data
        if not entry_data:
            abort(400)

        if not app_obj:
            db.create_app(app_id)

        if request.content_type == _JSON:
            db.add_app_entry(app_id, request.data.decode("utf-8"))
            return "yay!"
        elif request.content_type == _BINARY:
            abort(501)
        else:
            abort(400)


@app.route('/apps', methods=['GET'])
def show_apps() -> str:
    db = DataStore(DataStore.get_db_connection())
    apps = list(map(lambda x: x.json(), db.get_apps()))
    db.close()
    return json.dumps(apps)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')