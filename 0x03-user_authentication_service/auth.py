#!/usr/bin/env python3
"""
Auth Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """The returned bytes is a salted hash of the input
    password, hashed with bcrypt.hashpw"""
    salt = bcrypt.gensalt()
    pwd = password.encode('utf-8')
    h_pwd = bcrypt.hashpw(pwd, salt)

    return h_pwd
