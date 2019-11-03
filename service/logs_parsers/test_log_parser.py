from datetime import datetime

from service.logs_parsers.base import BaseParser


class TestLogParser(BaseParser):
    """
    Stub for testing purposes
    """

    def parse(self, log_line: str) -> dict:
        return {
            'date': datetime.today(),
            'level': 'INFO',
            'message': log_line,
        }
