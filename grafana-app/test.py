#!/usr/bin/env python3
import datetime
import sys
import unittest
import json
from unittest.mock import Mock

from db_connection import DBConnection
from models.query import Query
from models.query import ResponseEntry
from repository import data_store
from responder import Responder


class DatastoreTest(unittest.TestCase):

    def test_sql_datetime_from_unix(self) -> None:
        self.assertEqual('1990-02-27 00:00:00', self.data_store._sql_time_from_unix(636076800))

    def test_get_names(self) -> None:
        apps = self.data_store.get_app_names()
        self.assertEqual(['the app', 'the other app'], apps)
        self.assertTrue(self.data_store.get_app_names())

    def test_get_app_data(self) -> None:
        entries = self.data_store.get_app_data('the app')
        self.assertEqual(1, len(entries))
        self.assertEqual([['the app', datetime.datetime(1970, 1, 1, 0, 0, 2), 'fu']], entries)

    def test_get_app_data_for_interval(self) -> None:
        with self.conn as conn:
            conn.execute("insert into apps (id, description) values ('interval app', 'desc of test app')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1990-02-27 00:00:00', '1')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1991-02-27 00:00:00', '2')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1992-02-27 00:00:00', '2')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1993-02-27 00:00:00', '3')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('interval app', '1994-02-27 00:00:00', '4')")

        start = datetime.datetime(1991, 1, 1, 0, 0, 0)
        end = datetime.datetime(1993, 3, 1, 0, 0, 0)

        expected = [
            ['interval app', datetime.datetime(1991, 2, 27), '2'],
            ['interval app', datetime.datetime(1992, 2, 27), '2'],
            ['interval app', datetime.datetime(1993, 2, 27), '3']
        ]
        entries = self.data_store.get_app_data('interval app', start.timestamp(), end.timestamp())
        self.assertEqual(expected, entries)

    def test_get_empty_app_data(self) -> None:
        start = datetime.datetime(1990, 1, 1)
        end = datetime.datetime(1990, 1, 1)
        entries = self.data_store.get_app_data('interval app', start.timestamp(), end.timestamp())
        self.assertEqual([], entries)

    def tearDown(self) -> None:
        with self.conn as conn:
            conn.execute("DELETE FROM app_data")
            conn.execute("DELETE FROM apps")

    def setUp(self) -> None:
        with self.conn as conn:
            conn.execute("insert into apps (id, description) values ('the app', 'desc of test app')")
            conn.execute("insert into apps (id, description) values ('the other app', 'desc of the other app')")
            conn.execute("insert into app_data (app_id, created, txt) values ('the app', '1970-01-01 00:00:02', 'fu')")
            conn.execute(
                "insert into app_data (app_id, created, txt) values ('the other app', '1970-01-01 00:00:01','bar')")

    @classmethod
    def setUpClass(cls) -> None:
        cls.conn = DBConnection(conn_str)
        cls.data_store = data_store.DataStore(cls.conn)


class ResponseTest(unittest.TestCase):

    def test_search_gets_all_app_names(self) -> None:
        self.ds.get_app_names.return_value = ['a', 'b']
        self.assertEqual(self.responder.search(), ['a', 'b'])

    def test_query_for_timeserie_gets_all_data(self) -> None:
        hour_in_ms = 3600000
        q1 = Query({
            'intervalMs': hour_in_ms,
            'targets': [
                {
                    'target': 'fubar',
                    'type': 'timeserie'
                }
            ],
            'maxDataPoints': 5,
            'range': {
                'from': "2020-01-01T12:00:00.000Z",
                'to': "2020-01-04T12:00:00.000Z"
            }
        })
        expected = [
            {
                'datapoints': [
                    ['fu', 1577880000000],
                    ['fu', 1577880000000],
                    ['fu', 1577880000000],
                    ['fu', 1577880000000],
                    ['fu', 1577880000000]
                ],
                'target': 'fubar'
            }
        ]
        self.assertEqual(expected, self.responder.query(q1))

    def test_query_for_table_gets_all_data(self) -> None:
        hour_in_ms = 3600000
        q1 = Query({
            'intervalMs': hour_in_ms,
            'targets': [
                {
                    'target': 'fubar',
                    'type': 'table'
                }
            ],
            'maxDataPoints': 5,
            'range': {
                'from': "2020-01-01T12:00:00.000Z",
                'to': "2020-01-04T12:00:00.000Z"
            }
        })
        expected = [
            {
                'type': 'table',
                'columns': [
                    {
                        'text': 'dms_id',
                        'type': 'string',
                    },
                    {
                        'text': 'dms_time',
                        'type': 'time',
                    },
                    {
                        'text': 'data',
                        'type': 'string',
                    },
                ],
                'rows': [
                    ['the app', 1577880000000, 'fu'],
                    ['the app', 1577880000000, 'fu'],
                    ['the app', 1577880000000, 'fu'],
                    ['the app', 1577880000000, 'fu'],
                    ['the app', 1577880000000, 'fu']
                ],
            }
        ]
        self.assertEqual(expected, self.responder.query(q1))

    def setUp(self) -> None:
        self.ds = Mock()
        self.ds.get_app_data.return_value = [
            ('the app', datetime.datetime(2020, 1, 1, 4), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 4), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 4), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 4), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 4), 'fu')
        ]
        self.responder = Responder(self.ds)


class ResponseJsonTest(unittest.TestCase):

    def test_query_for_table_gets_all_json_data(self) -> None:
        hour_in_ms = 3600000
        q1 = Query({
            'intervalMs': hour_in_ms,
            'targets': [
                {
                    'target': 'fubar',
                    'type': 'table'
                }
            ],
            'maxDataPoints': 5,
            'range': {
                'from': "2020-01-01T12:00:00.000Z",
                'to': "2020-01-04T12:00:00.000Z"
            }
        })
        expected = [
            {
                'type': 'table',
                'columns': [
                    {
                        'text': 'dms_id',
                        'type': 'string',
                    },
                    {
                        'text': 'dms_time',
                        'type': 'time',
                    },
                    {
                        'text': 'inner.fu',
                        'type': 'string',
                    },
                    {
                        'text': 'inner.bar',
                        'type': 'number',
                    },
                    {
                        'text': 'outer',
                        'type': 'number',
                    }
                ],
                'rows': [
                    ['the app', 1577880000000, 'bar', 2, 123.4],
                    ['the app', 1577880000000, 'bar', 2, 123.4],
                    ['the app', 1577880000000, 'bar', 2, 123.4],
                    ['the app', 1577880000000, 'bar', 2, 123.4],
                    ['the app', 1577880000000, 'bar', 2, 123.4]
                ],
            }
        ]
        #print(expected)
        #print("==============================")
        #print(self.responder.query(q1))
        self.maxDiff = None
        self.assertEqual(expected, self.responder.query(q1))

    def setUp(self) -> None:

        j_data = json.dumps({
            'inner': {
                'fu': 'bar',
                'bar': 2
            },
            'outer': 123.4
        })

        self.ds = Mock()
        self.ds.get_app_data.return_value = [
            ('the app', datetime.datetime(2020, 1, 1, 4), j_data),
            ('the app', datetime.datetime(2020, 1, 1, 4), j_data),
            ('the app', datetime.datetime(2020, 1, 1, 4), j_data),
            ('the app', datetime.datetime(2020, 1, 1, 4), j_data),
            ('the app', datetime.datetime(2020, 1, 1, 4), j_data)
        ]
        self.responder = Responder(self.ds)

class QueryTest(unittest.TestCase):

    def test_filter(self):
        data = [
            ('the app', datetime.datetime(2019, 1, 1, 1), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 1), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 2, 30), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 3), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 4), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 5), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 6), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 7), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 8), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 9), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 10), 'fu'),
            ('the app', datetime.datetime(2021, 1, 1, 11), 'fu')
        ]

        expected = [
            ('the app', datetime.datetime(2020, 1, 1, 2, 30), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 4), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 6), 'fu'),
            ('the app', datetime.datetime(2020, 1, 1, 8), 'fu')
        ]

        date_from = datetime.datetime(2020, 1, 1)
        date_to = datetime.datetime(2020, 4, 1)
        hour_in_ms = 3600000

        q = ResponseEntry(Mock(), 'bob', date_from.timestamp(), date_to.timestamp(), hour_in_ms, 4)
        filtered = q._get_filtered(data, 1)

        self.assertEqual(expected, filtered)

    def test_parse_entry(self):

        data = {
            'attr': {
                'inner': 'fu',
                'v': 1
            },
            'bar': 'fubar'
        }
        exp = {
            'attr.inner': 'fu',
            'attr.v': 1,
            'bar': 'fubar'
        }
        q = ResponseEntry(Mock(), 'bob', 0, 0, 0, 4)
        self.assertEqual(exp, q._key_vals_to_path_vals(data, '.'))

    def test_is_json(self):
        q = ResponseEntry(Mock(), 'bob', 0, 0, 0, 4)
        self.assertFalse(q._is_json('2'))
        self.assertFalse(q._is_json('lol'))
        self.assertFalse(q._is_json('{'))
        self.assertFalse(q._is_json('}'))
        self.assertTrue(q._is_json('{}'))


if __name__ == '__main__':
    conn_str = sys.argv.pop()  # Hacky, but prefer being able to dynamically parse the conn string for DB tests
    unittest.main()
