#!/usr/bin/env python3
""" Auth class for API authentication
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """ Template for authentication system """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required.
        
        Args:
            path (str): The requested path.
            excluded_paths (List[str]): A list of paths that don't require authentication.
        
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        # If path is None or excluded_paths is None or empty, authentication is required
        if path is None or excluded_paths is None:
            return True

        # Normalize the path by removing trailing slashes
        normalized_path = path.rstrip('/')

        # Check if the normalized path is in excluded_paths (also normalize each entry)
        for excluded in excluded_paths:
            if normalized_path == excluded.rstrip('/'):
                return False

        # Authentication is required if path isn't in excluded_paths
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.
        
        Args:
            request: The Flask request object.
        
        Returns:
            str: The value of the authorization header, or None if it's not present.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar:
        """
        Retrieves the current user.
        
        Args:
            request: The Flask request object.
        
        Returns:
            TypeVar('User'): This method should be overridden in subclasses. Defaults to None.
        """
        # This method should be overridden in subclasses to retrieve the actual user.
        return None
