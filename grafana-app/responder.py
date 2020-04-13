from db_connection import DBConnection
from models.annotation import Annotation
from models.query import Query
from models.query import ResponseEntry
from repository.data_store import DataStore


class Responder:

    @staticmethod
    def get_data_store() -> DataStore:
        #TODO: Make env variable
        #return DataStore(DBConnection("dbname='dms' user='root' password='root' host='flask_db' port='5432'"))
        return DataStore(DBConnection("postgresql://flask_db:5432/dms?user=root&password=root"))

    def __init__(self, data_store: DataStore):
        self._data_store = data_store

    def query(self, query: Query) -> list:

        _TIME_SERIE = "timeserie"
        _TABLE = "table"

        resp = []

        for target in query.get_targets():
            if target.get_type() == _TIME_SERIE:
                resp.append(
                    ResponseEntry(
                        self._data_store,
                        target.get_name(),
                        *query.get_unix_range(),
                        query.get_ms_interval(),
                        query.get_max_datapoint_count()
                    ).as_time_series()
                )
            elif target.get_type() == _TABLE:
                resp.append(
                    ResponseEntry(
                        self._data_store,
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

    def annotation(self, annotation: Annotation) -> list:
        # TOTO: Implement this. Empty response for now
        rsp_annotations = []
        return rsp_annotations

    def search(self) -> list:
        # Get all names
        return self._data_store.get_app_names()
