#!/usr/bin/env python3
"""
A module with a function called filter_datum
"""
import re
import logging
from typing import List
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


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
    log_pii = logging.getLogger(name)
    log_pii.setLevel(logging.INFO)
    log_pii.propagate = False

    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    log_pii.addHandler(stream)

    return log_pii


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    USER = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    PASSWORD = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    HOST = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    MY_DB = os.getenv('PERSONAL_DATA_DB_NAME')

    my_db = mysql.connector.connection.MySQLConnection(user=USER,
                                                       password=PASSWORD,
                                                       host=HOST,
                                                       database=MY_DB)

    return my_db


def main():
    """will obtain a database connection using get_db and retrieve
    all rows in the users table and display each row under
    a filtered format"""
    get_users = get_db()
    cursor = get_users.cursor()

    cursor.execute('SELECT * FROM users;')

    field_names = [f[0] for f in cursor.description]
    log_pii = get_logger()

    for r in cursor:
        infos = ''
        for x, y in zip(r, field_names):
            infos += f'{y}={(x)};'
        log_pii.info(infos)

    cursor.close()


if __name__ == '__main__':
    main()
