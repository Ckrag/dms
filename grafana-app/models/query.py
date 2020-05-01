import json
import numbers
from datetime import datetime

from repository.data_store import DataStore
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

        data_points = [[data[2], int(data[1].timestamp() * 1000)] for data in self._get_filtered(app_data)]

        # Filter data points
        # Ensure none bigger than large

        return {
            'target': self.name,
            'datapoints': data_points
        }

    def as_table(self) -> dict:
        data = self.data_store.get_app_data(self.name, self.interval_from, self.interval_to)
        filtered_data = self._get_filtered(data)
        # Strong assumption here that all entries have identical attributes.
        # If anything fails, default to standard response
        # TODO: Enforce structure on data from DMS-ingest instead of implementing error handling here
        # TODO: Expose fields for with each endpoint, removing need for this fuckery

        if filtered_data and self._is_json(filtered_data[0][2]):
            return self._make_table_json(filtered_data)
        else:
            return self._make_table_simple(filtered_data)

    def _make_table_simple(self, data: list) -> dict:
        return {
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
            'rows': [[t[0], int(t[1].timestamp() * 1000), t[2]] for t in data]
        }

    def _make_table_json(self, data: list) -> dict:
        # Strong assumption here that all entries have identical attributes.
        # If anything fails, default to standard response
        # TODO: Enforce structure on data from DMS-ingest instead of implementing error handling here
        # TODO: Expose fields for with each endpoint, removing need for this fuckery
        resp = {
            'type': 'table',
            'columns': [
                {
                    'text': 'dms_id',
                    'type': 'string',
                },
                {
                    'text': 'dms_time',
                    'type': 'time',
                }
            ],
            'rows': []
        }
        columns_complete = False
        for entry in data:
            data_dict = json.loads(entry[2])
            paths = self._key_vals_to_path_vals(data_dict)
            table_row_entries = []
            for p, v in paths.items():
                table_row_entries.append(v)
                if columns_complete:
                    continue
                # Removable when above TODOs done..
                c = {
                    'text': p,
                    # TODO: Handle time type..
                    'type': 'number' if isinstance(v, numbers.Number) else 'string'
                }
                if c not in resp['columns']:
                    resp['columns'].append(c)
            columns_complete = True
            resp['rows'].append([entry[0], int(entry[1].timestamp() * 1000), *table_row_entries])

        return resp

    def _is_json(self, data: str) -> bool:
        if not '{' in data:
            return False
        try:
            json.loads(data)
        except ValueError:
            return False
        return True

    def _get_filtered(self, data_points: list, margin=1.2) -> list:
        date_from = datetime.fromtimestamp(self.interval_from)
        date_to = datetime.fromtimestamp(self.interval_to)

        if len(data_points) <= self.max_data_points:
            return data_points  # Should still do fine, we'll see

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
            if divmod(i + 1, nth_required_delete)[1] != 0:
                fitted_data.append(data)

        return fitted_data

    def _key_vals_to_path_vals(self, entry: dict, delimiter='.', base='', paths=None) -> dict:
        if paths is None:
            paths = {}
        for k, v in entry.items():
            if isinstance(v, dict):
                n_base = str(k) if len(base) == 0 else base + delimiter + str(k)
                self._key_vals_to_path_vals(v, delimiter, n_base, paths)
            else:
                n_base = '' if len(base) == 0 else base + delimiter
                paths[n_base + str(k)] = v
        return paths
