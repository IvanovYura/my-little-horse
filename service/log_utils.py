import datetime
import re
from typing import List

# TODO: beautify REGEXP
LOG_LINE_REGEXP = '([0-9.]+)[\s-]{2,}\s\[(.*)\s.*\]\s\"(.*?)\s(.*?)\sHTTP.*\"\s(.*?)\s(.*?)\s\"(.*?)\"\s\"(.*?)\"'
LOG_DATE_TIME_FORMAT = '%d/%b/%Y:%H:%M:%S'


def get_logs(path_to_log: str, date_from: str, date_to: str) -> List[dict]:
    """
    Returns the list of log entries from the log file.

    The log entries should be in appropriate format.
    """
    result = []
    with open(path_to_log) as lines:
        for line in lines:
            groups = re.search(LOG_LINE_REGEXP, line).groups()
            result.append({
                'host_ip': groups[0],
                'timestamp': _get_date_time(groups[1]),
                'verb': groups[2],
                'path': groups[3],
                'code': groups[4],
                'user_agent': groups[-1],
            })
    return result


def _get_date_time(date_time: str) -> datetime:
    return datetime.datetime.strptime(date_time, LOG_DATE_TIME_FORMAT)
