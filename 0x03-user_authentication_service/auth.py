#!/usr/bin/env python3
"""
Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """return a User object"""
        try:
            reg_user = self._db.find_user_by(email=email)
            if reg_user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            h_pwd = _hash_password(password)
            new_user = self._db.add_user(email, h_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """return True. In any other case, return False."""
        try:
            ex_user = self._db.find_user_by(email=email)

            if ex_user:
                pwd = password.encode()
                val_pwd = ex_user.hashed_password
                if bcrypt.checkpw(pwd, val_pwd):
                    return True
            return False
        except NoResultFound:
            return False


def _hash_password(password: str) -> bytes:
    """The returned bytes is a salted hash of the input
    password, hashed with bcrypt.hashpw"""
    salt = bcrypt.gensalt()
    pwd = password.encode('utf-8')
    h_pwd = bcrypt.hashpw(pwd, salt)

    return h_pwd
