#!/usr/bin/env python3
"""
Module for log message obfuscation with logging formatter.
"""

import logging
from typing import List

# Assume filter_datum is imported or defined here
def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class to obfuscate sensitive information """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Apply redaction to the log message before formatting."""
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)
