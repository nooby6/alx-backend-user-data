#!/usr/bin/env python3
"""
Module for log message obfuscation.
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replaces values of specified fields in a log message with a redaction string.
    
    Args:
        fields (List[str]): Fields to obfuscate in the message.
        redaction (str): String to replace the field values with.
        message (str): The log message.
        separator (str): The separator character between fields.
    
    Returns:
        str: The log message with specified fields redacted.
    """
    pattern = f'({"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

