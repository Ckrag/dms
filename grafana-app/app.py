import json

from flask import Flask
from flask import request

from models.annotation import Annotation
from models.query import Query
from response import Response

import json

# http://www.oznetnerd.com/writing-a-grafana-backend-using-the-simple-json-datasource-flask/
# https://github.com/grafana/simple-json-datasource
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health():
    return {}, 200


@app.route('/search', methods=['POST'])
def search():
    # Liste of named services
    targets = []

    return json.dumps(Response.search()), 200


@app.route('/query', methods=['GET'])
def query():
    grafana_query = json.loads(request.data.decode("utf-8"))
    g_query = Query(grafana_query)

    return json.dumps(Response.query(g_query)), 200


@app.route('/annotations', methods=['GET'])
def annotations():
    grafana_annotation = json.loads(request.data.decode("utf-8"))
    annotation = Annotation(grafana_annotation)
    return json.dumps(Response.annotation(annotation)), 200


if __name__ == '__main__':
    app.run()
