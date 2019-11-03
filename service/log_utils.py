from typing import List

from service.logs_parsers.access_log_parser import AccessLogParser
from service.logs_parsers.test_log_parser import TestLogParser

access_log_parser = AccessLogParser()
test_log_parser = TestLogParser()


def get_logs(path_to_log: str, date_from: str, date_to: str) -> List[dict]:
    """
    Returns the list of log entries from the log file.

    The log entries should be in appropriate format.
    """
    result = []

    if date_from > date_to:
        raise ValueError('Date "from" time should be in the past')

    with open(path_to_log) as lines:
        for line in lines:
            entry = access_log_parser.parse(line)

            if entry:
                result.append(
                    access_log_parser.filter_log_entry(entry, date_from, date_to),
                )

    return result


def get_test_logs() -> List[dict]:
    test_parser = TestLogParser()
    return [test_parser.parse('A test message')]
