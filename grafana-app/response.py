from db_connection import DBConnection
from models.annotation import Annotation
from models.query import Query
from models.query import ResponseEntry
from repository.data_store import DataStore


class Response:

    @staticmethod
    def _get_data_store() -> DataStore:
        #return DataStore(DBConnection("dbname='dms' user='root' password='root' host='flask_db' port='5432'"))
        return DataStore(DBConnection("postgresql://flask_db:5432/dms?user=root&password=root"))

    @staticmethod
    def query(query: Query) -> list:

        _TIME_SERIE = "timeserie"
        _TABLE = "table"

        data_store = Response._get_data_store()

        resp = []

        for target in query.get_targets():
            if target.get_type() == _TIME_SERIE:
                resp.append(
                    ResponseEntry(
                        data_store,
                        target.get_name(),
                        *query.get_unix_range(),
                        query.get_ms_interval(),
                        query.get_max_datapoint_count()
                    ).as_time_series()
                )
            elif target.get_type() == _TABLE:
                resp.append(
                    ResponseEntry(
                        data_store,
                        target.get_name(),
                        *query.get_unix_range(),
                        query.get_ms_interval(),
                        query.get_max_datapoint_count()
                    ).as_table()
                )
            else:
                err_str = "Unable to respond to query for {} of type {}, with timeframe {} to {}".format(
                    target.get_name(),
                    target.get_type(),
                    *query.get_unix_range()
                )
                print(err_str)
                resp = None

        return resp

    @staticmethod
    def annotation(annotation: Annotation) -> list:
        # TOTO: Implement this. Empty response for now
        rsp_annotations = []
        return rsp_annotations

    @staticmethod
    def search() -> list:
        # Get all names
        return Response._get_data_store().get_app_names()
