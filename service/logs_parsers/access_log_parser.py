import re
from typing import Optional

from service.logs_parsers.base import BaseParser
from service.utils import get_date_time


class AccessLogParser(BaseParser):
    LOG_LINE_REGEXP = (
        '(?P<host_ip>[0-9.]+)[\s-]{2,}\s\['
        '(?P<timestamp>[0-9a-zA-z/:]+)\s\S+]\s\"'
        '(?P<verb>[A-Z]+)\s'
        '(?P<path>[0-9a-zA-Z/.]+)\s\S+\"\s'
        '(?P<code>\d+)\s\d+\s\"[\S]+\"\s\"'
        '(?P<user_agent>.*?)\"'
    )

    # because for each log date can be in any format
    LOG_DATE_TIME_FORMAT = '%d/%b/%Y:%H:%M:%S'

    def parse(self, log_line: str) -> dict:
        """
        Returns log entry as dictionary
        """
        groups = re.search(self.LOG_LINE_REGEXP, log_line)

        return groups.groupdict() if groups else {}

    def filter_log_entry(self, entry: dict, date_from: str, date_to: str) -> Optional[dict]:
        """
        Filters the log entry by start and end dates
        """
        date_from_dt = get_date_time(date_from, self.DATE_FORMAT)
        date_to_dt = get_date_time(date_to, self.DATE_FORMAT)

        timestamp = get_date_time(entry['timestamp'], self.LOG_DATE_TIME_FORMAT)

        if date_from_dt <= timestamp <= date_to_dt:
            entry['timestamp'] = timestamp
            return entry

        return None
