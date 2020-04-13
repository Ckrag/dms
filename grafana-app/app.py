import json

from flask import Flask
from flask import request
import flask

from models.annotation import Annotation
from models.query import Query
from responder import Responder

# http://www.oznetnerd.com/writing-a-grafana-backend-using-the-simple-json-datasource-flask/
# https://github.com/grafana/simple-json-datasource
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health():
    return '{}', 200


@app.route('/search', methods=['POST'])
def search():
    # Liste of named services
    responder = Responder(Responder.get_data_store())
    return json.dumps(responder.search()), 200


@app.route('/query', methods=['GET'])
def query():
    grafana_query = json.loads(request.data.decode("utf-8"))
    g_query = Query(grafana_query)

    responder = Responder(Responder.get_data_store())
    resp = responder.query(g_query)
    return (json.dumps(resp), 200) if resp else flask.abort(500)


@app.route('/annotations', methods=['GET'])
def annotations():
    grafana_annotation = json.loads(request.data.decode("utf-8"))
    annotation = Annotation(grafana_annotation)
    responder = Responder(Responder.get_data_store())
    return json.dumps(responder.annotation(annotation)), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')