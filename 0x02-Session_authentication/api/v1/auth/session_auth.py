#!/usr/bin/env python3
""" Module of session_auth views
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """creating a new authentication mechanism"""
