#!/usr/bin/python3

from flask import Flask
from flask import request

app = Flask(__name__)

# https://medium.com/@shamir.stav_83310/dockerizing-a-flask-mysql-app-with-docker-compose-c4f51d20b40d

_JSON = "application/json"
_BINARY = "multipart/form-data "


@app.route('/<string:app_id>', methods=['POST'])
def receive_data(app_id):
    if request.content_type == _JSON:
        pass
    elif request.content_type == _BINARY:
        pass
    else:
        pass #TODO: Not recognized; HTTP ERROR

    print(request.content_type)
    return "Running: {}".format(app_id)


@app.route('/apps', methods=['GET'])
def show_apps():
    return "TODO: Give app info"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
