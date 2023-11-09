#!/usr/bin/env python3
""" Module of auth views
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """class that is auth methods for our app"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns True if the path is not in the list of
        strings excluded_paths"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """validate all requests to secure the API"""
        if request is None:
            return None
        handling = request.headers.get('Authorization', None)
        return handling

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        sess_env = os.getenv('SESSION_NAME')
        sess_cookie = request.cookies.get(sess_env)

        return sess_cookie
