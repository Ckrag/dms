import unittest


class BaseTest(unittest.TestCase):

    def runTest(self):
        test_methods = [method_name for method_name in dir(self)
                        if method_name.startswith('test') and callable(getattr(self, method_name))]
        for method in test_methods:
            getattr(self, method)()