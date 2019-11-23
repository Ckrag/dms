from util import Util


class Query:
    _ms_interval = None
    _targets = None
    _max_data_points = None
    _interval_from = None
    _interval_to = None

    def __init__(self, query_data: dict):
        self._ms_interval = query_data['intervalMs']
        self._targets = [Target(target) for target in query_data['targets']]
        self._max_data_points = query_data['maxDataPoints']
        self._interval_from = query_data['range']['from']
        self._interval_to = query_data['range']['to']

    def get_ms_interval(self) -> int:
        """
        :return: Expected interval between each data entry, in millisecs
        """
        return self._ms_interval

    def get_targets(self) -> list:
        return self._targets

    def get_max_datapoint_count(self) -> int:
        """
        :return: Maximum number of allowed data-points
        """
        return self._max_data_points

    def get_unix_range(self) -> tuple:
        return Util.iso_to_unix(self._interval_from), Util.iso_to_unix(self._interval_to)


class Target:
    _name = None
    _type = None

    def __init__(self, query_data: dict):
        self._name = query_data['target']
        self._type = query_data['type']

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> str:
        return self._type


class TimeSerie:

    def __init__(self, name: str, interval_from: int, interval_to: int):
        pass

    def as_response(self) -> dict:
        return {}


class Table:

    def __init__(self, name: str, interval_from: int, interval_to: int):
        pass

    def as_response(self) -> dict:
        return {}
