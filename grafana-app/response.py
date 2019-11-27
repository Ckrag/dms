from models.annotation import Annotation
from models.query import Query
from models.query import TimeSerie, Table

import psycopg2

class Response:

    @staticmethod
    def query(query: Query) -> list:

        _TIME_SERIE = "timeserie"
        _TABLE = "table"

        resp = []

        for target in query.get_targets():
            if target.get_type() == _TIME_SERIE:
                resp.append(
                    TimeSerie(target.get_name(), *query.get_unix_range())
                )
            elif target.get_type() == _TABLE:
                resp.append(
                    Table(target.get_name(), *query.get_unix_range()).as_response()
                )
            else:
                err_str = "Unable to respond to query for {} of type {}, with timeframe {} to {}".format(
                    target.get_name(),
                    target.get_type(),
                    *query.get_unix_range()
                )
                print(err_str)

        return resp

    @staticmethod
    def annotation(annotation: Annotation) -> list:
        # TOTO: Implement this. Empty response for now
        rsp_annotations = []
        return rsp_annotations

    @staticmethod
    def search() -> list:
        # Get all names

        

        return []
