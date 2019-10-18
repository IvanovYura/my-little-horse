from datetime import datetime


def get_date_time(date_time: str, fmt: str) -> datetime:
    """
    Formats input string as per passed format string.
    """
    return datetime.strptime(date_time, fmt)
