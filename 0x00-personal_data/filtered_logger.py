#!/usr/bin/env python3
"""
A module with a function called filter_datum
"""
import re
import logging
from typing import List


PII_FIELDS = ('name', 'ssn', 'password', 'email', 'phone')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for fx in fields:  # this is ex: {fx} is password=.+?(reexp);(separator)
        message = re.sub(f'{fx}=.+?{separator}',
                         f'{fx}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init method for class RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """to filter values in incoming log records using filter_datum"""
        # rec = record.__dict__
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(),
                                  RedactingFormatter.SEPARATOR)
        # Super from parent class logging.Formatter and pass in the child cl
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    name = "user_data"

    log_pii = logging.get_logger(name)
    logger.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter)
    logger.addHandler(stream)

    return log_pii
