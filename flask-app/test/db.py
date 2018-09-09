from data.data_store import DataStore
import psycopg2


def get_database() -> DataStore:
    return DataStore(DataStore.get_db_connection(get_db_test_connect_string()))


def get_db_test_connect_string() -> str:
    return "dbname='dms' user='root' password='root' host='0.0.0.0' port='5432'"