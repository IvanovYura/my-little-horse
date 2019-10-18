class BaseParser:
    """
    Abstract class for parsers
    """

    LOG_LINE_REGEXP: str

    def parse(self, log_line: str) -> dict:
        """
        Should be implemented in your parser subclass.
        The return value should be a valid JSON-serializable object.
        """
        raise NotImplementedError
