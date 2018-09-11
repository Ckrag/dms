#!/usr/bin/python3

from flask import Flask
from flask import abort
from flask import request
from flask import make_response

from model.dms import DMS as DMS_APPLICATION

app = Flask(__name__)

# https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d
# http://flask.pocoo.org/docs/1.0/quickstart/#about-responses

_JSON = "application/json"
_BINARY = "multipart/form-data "

DMS = DMS_APPLICATION()


@app.route('/app/<string:app_id>', methods=['POST'])
def receive_data(app_id: str) -> str or int:
    app_id = app_id.lower()

    rsp = DMS.on_data_received(app_id, request.data.decode("utf-8"), request.content_type)

    if rsp >= 400:
        abort(rsp)
    else:
        return "{} entry added".format(app_id)  # 200


@app.route('/app/<string:app_id>', methods=['DELETE'])
def delete_app(app_id: str) -> str or int:
    app_id = app_id.lower()

    DMS.on_app_delete(app_id)
    return "{} Deleted".format(app_id)  # 200


@app.route('/app/<string:app_id>', methods=['GET'])
def show_app(app_id: str) -> str:

    app_data = DMS.on_app_requested(app_id)

    if isinstance(app_data, int):
        abort(404) # if I use the app_data var it inf. recurses #TODO: Fix this
    else:
        resp = make_response(app_data)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['charset'] = 'utf-8'
        return resp


@app.route('/entries/<string:app_id>', methods=['GET'])
def show_entries(app_id: str):
    app_id = app_id.lower()

    resp = make_response(DMS.on_entries_requested(app_id))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['charset'] = 'utf-8'
    return resp


@app.route('/apps', methods=['GET'])
def show_apps():
    resp = make_response(DMS.on_apps_requested())
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['charset'] = 'utf-8'
    return resp


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
