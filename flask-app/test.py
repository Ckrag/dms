import sys
import unittest

from test import test_app


def other_create_suite(conn_str: str):
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_app.DBTest(conn_str))
    return test_suite


if __name__ == '__main__':
    db_conn_str = sys.argv.pop()  # Hacky, but prefer being able to dynamically parse the conn string for DB tests
    suite = other_create_suite(db_conn_str)
    runner = unittest.TextTestRunner()
    runner.run(suite)
