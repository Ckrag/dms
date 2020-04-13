from repository.data_store import DataStore
from datetime import datetime, timedelta
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

    def __init__(self, query_data: dict):
        self._name = query_data['target']
        self._type = query_data['type']

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> str:
        return self._type


class ResponseEntry:

    def __init__(self, data_store: DataStore, name: str, interval_from: int, interval_to: int, ms_interval: int,
                 max_data_point: int):
        self.name = name
        self.interval_from = interval_from
        self.interval_to = interval_to
        self.ms_interval = ms_interval
        self.max_data_points = max_data_point
        self.data_store = data_store

    def as_time_series(self) -> dict:
        app_data = self.data_store.get_app_data(self.name, self.interval_from, self.interval_to)

        data_points = [data[2] for data in self._get_filtered(app_data)]

        # Filter data points
        # Ensure none bigger than large

        return {
            'target': self.name,
            'data_points': data_points
        }

    def as_table(self) -> dict:
        data = self.data_store.get_app_data(self.name, self.interval_from, self.interval_to)
        return {
            'type': 'table',
            'columns': ['id', 'created', 'data'],
            'rows': [list(t) for t in self._get_filtered(data)]
        }

    def _get_filtered(self, data_points: list, margin=1.2) -> list:
        date_from = datetime.fromtimestamp(self.interval_from)
        date_to = datetime.fromtimestamp(self.interval_to)

        if len(data_points) <= self.max_data_points:
            return data_points # Should still do dine, we'll see

        # Filter outside interval
        interval_data = [x for x in data_points if date_from <= x[1] <= date_to]

        # Filter clustered data
        spaced_data = []
        i = 0
        while i < len(interval_data) - 1:
            interval = (interval_data[i + 1][1] - interval_data[i][1]).total_seconds() * 1000
            if interval <= self.ms_interval * margin:
                spaced_data.append(interval_data[i])
            i += 1

        # Evenly remove to get requested number
        overflow = abs(len(spaced_data) - self.max_data_points)
        if overflow <= 0:
            return spaced_data
        nth_required_delete = 1 / (overflow / len(spaced_data))
        fitted_data = []
        for i, data in enumerate(spaced_data):
            if divmod(i+1, nth_required_delete)[1] != 0:
                fitted_data.append(data)

        return fitted_data
