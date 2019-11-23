from datetime import datetime


class Util:

    @staticmethod
    def iso_to_unix(dt_format: str) -> int:
        utc_dt = datetime.strptime(dt_format, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Convert UTC datetime to seconds since the Epoch
        timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
        return int(timestamp)
