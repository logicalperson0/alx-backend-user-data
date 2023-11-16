#!/usr/bin/env python3
"""
Auth Module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


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

    def create_session(self, email: str) -> str:
        """returns the session ID as a string"""
        try:
            ex_user = self._db.find_user_by(email=email)
            if ex_user:
                sess_id = _generate_uuid()
                ex_user.session_id = sess_id
                return sess_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """returns the corresponding User or None"""
        if session_id is None:
            return None
        try:
            ex_user = self._db.find_user_by(session_id=session_id)
            return ex_user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """The method updates the corresponding user’s session ID to None"""
        # self._db.update_user(user_id, session_id=None)
        try:
            des_user = self._db.find_user_by(id=user_id)
            if des_user:
                des_user.session_id = None
                return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generate a UUID and update the user’s
        reset_token database field"""
        try:
            get_user = self._db.find_user_by(email=email)
            if get_user:
                token = _generate_uuid()
                get_user.reset_token = token
                return token
        except Exception:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """The returned bytes is a salted hash of the input
    password, hashed with bcrypt.hashpw"""
    salt = bcrypt.gensalt()
    pwd = password.encode('utf-8')
    h_pwd = bcrypt.hashpw(pwd, salt)

    return h_pwd


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())
