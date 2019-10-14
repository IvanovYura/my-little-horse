import datetime
import re
from typing import List

LOG_LINE_REGEXP = (
    '(?P<ip>[0-9.]+)[\s-]{2,}\s\['
    '(?P<timestamp>[0-9a-zA-z/:]+)\s\S+]\s\"'
    '(?P<verb>[A-Z]+)\s'
    '(?P<path>[0-9a-zA-Z/.]+)\s\S+\"\s'
    '(?P<code>\d+)\s\d+\s\"[\S]+\"\s\"'
    '(?P<ua>.*?)\"'
)

LOG_DATE_TIME_FORMAT = '%d/%b/%Y:%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


def get_logs(path_to_log: str, date_from: str, date_to: str) -> List[dict]:
    """
    Returns the list of log entries from the log file.

    The log entries should be in appropriate format.
    """
    result = []

    date_from = _get_date_time(date_from, DATE_FORMAT)
    date_to = _get_date_time(date_to, DATE_FORMAT)

    if date_from > date_to:
        raise ValueError('Date "from" time should be in the past')

    with open(path_to_log) as lines:
        for line in lines:
            entry = _filter_by_date(line, date_from, date_to)

            if entry:
                result.append(entry)

    return result


def _filter_by_date(line, date_from: datetime, date_to: datetime) -> dict:
    """
    Filters the log line by start and end dates.

    Returns the filtered line as dictionary.
    """
    groups = re.search(LOG_LINE_REGEXP, line).groups()
    timestamp = _get_date_time(groups[1], LOG_DATE_TIME_FORMAT)

    entry = {
        'host_ip': groups[0],
        'timestamp': timestamp,
        'verb': groups[2],
        'path': groups[3],
        'code': groups[4],
        'user_agent': groups[-1],
    }

    if date_from <= timestamp <= date_to:
        return entry


def _get_date_time(date_time: str, fmt: str) -> datetime:
    """
    Formats input string as per passed format string.
    """
    return datetime.datetime.strptime(date_time, fmt)
