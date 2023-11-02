#!/usr/bin/env python3
"""
module with the hash_password function with bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string using
    bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """to validate that the provided password matches the hashed
    password and return a boolean value"""
    check_pwd = bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    if check_pwd:
        return True
    return False
