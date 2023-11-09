#!/usr/bin/env python3
""" Module of session_auth views
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """creating a new authentication mechanism"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or type(user_id) != str:
            return None
        sess_id = str(uuid4())
        self.user_id_by_session_id[sess_id] = user_id

        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""

        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """(overload) that returns a User instance based on a cookie value"""
        sess_id = self.session_cookie(request)
        curr_id = self.user_id_for_session_id(sess_id)
        user_by_id = User.get(curr_id)

        return user_by_id
