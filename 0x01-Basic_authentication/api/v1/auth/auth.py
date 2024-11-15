#!/usr/bin/env python3
""" Auth class for API authentication
"""
from flask import request
from typing import List, TypeVar
import jwt

class Auth:
    """ Template for authentication system """
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required
        Args:
            path (str): the requested path
            excluded_paths (List[str]): a list of paths that don't require authentication
        Returns:
            bool: True if authentication is required, False if not
        """
        if path is None or not excluded_paths:
            return True
        
        # Normalize path and excluded paths to be slash-tolerant
        normalized_path = path.rstrip('/')
        for excluded in excluded_paths:
            if normalized_path == excluded.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        Args:
            request: the Flask request object
        Returns:
            str: the Authorization header or None if not found
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user
        Args:
            request: the Flask request object
        Returns:
            TypeVar('User'): None if no user is authenticated
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        try:
            token = auth_header.split(" ")[1]  # Split "Bearer <token>"
            decoded_token = jwt.decode(token, "your_secret_key", algorithms=["HS256"])
            return decoded_token.get('user')  # Assuming the token contains user info
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
