#!/usr/bin/env python3
"""
Module for filtering and logging sensitive information.
"""

import os
import re
import logging
import mysql.connector
from typing import List
from mysql.connector.connection import MySQLConnection

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates fields in a log message.
    """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class for logging sensitive information. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)

def get_db() -> MySQLConnection:
    """
    Connects to the MySQL database using credentials from environment variables.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

def main() -> None:
    """
    Main function to retrieve all rows in the users table and display each row
    in a filtered format.
    """
    # Sensitive fields that need to be redacted
    sensitive_fields = ["name", "email", "phone", "ssn", "password"]

    # Set up logger
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(sensitive_fields))
    logger.addHandler(handler)

    # Connect to the database and retrieve user data
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users;")

    # Log each row with sensitive fields redacted
    for row in cursor:
        record = (
            f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]}; "
            f"password={row[4]}; ip={row[5]}; last_login={row[6]}; user_agent={row[7]}"
        )
        logger.info(record)

    # Close the cursor and database connection
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
