#!/usr/bin/env python3
"""Auth module for the API"""
from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch


class Auth():
    """Auth Class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Return True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if (path in excluded_paths or path[:-1] in excluded_paths or
                f"{path}/" in excluded_paths):
            return False

        for excluded_path in excluded_paths:
            if fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Return the generated authorization header string.
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.

        Args:
            request (Optional[Request]): The request object (default: None).

        Return the current user.

        """
        return None
