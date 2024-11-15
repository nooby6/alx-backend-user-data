#!/usr/bin/env python3
""" Auth class for API authentication
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """ Template for authentication system """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required
        Args:
            path (str): the requested path
            excluded_paths (List[str]): a list of paths that don't require authentication
        Returns:
            bool: False for now
        """
        # This method currently always returns False, meaning no authentication is required
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        Args:
            request: the Flask request object
        Returns:
            str: None for now
        """
        # This method currently always returns None, meaning no authorization header is retrieved
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user
        Args:
            request: the Flask request object
        Returns:
            TypeVar('User'): None for now
        """
        # This method currently always returns None, meaning no user is retrieved
        return None
