from util import Util


class Annotation:
    _interval_from = None
    _interval_to = None
    _received_annotation = None
    _name = None

    def __init__(self, annotation_data: dict):
        self._interval_from = annotation_data['range']['from']
        self._interval_to = annotation_data['range']['to']
        self._received_annotation = annotation_data['annotation']
        self._name = annotation_data['annotation']['name']

    def get_unix_range(self) -> tuple:
        return Util.iso_to_unix(self._interval_from), Util.iso_to_unix(self._interval_to)

    def get_grafana_annotation(self) -> dict:
        return self._received_annotation

    def get_name(self) -> str:
        return self._name
