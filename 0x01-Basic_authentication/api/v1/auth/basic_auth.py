#!/usr/bin/env python3
""" Module of basic_auth views
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """class BasicAuth that inherits from Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization
        header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            valid_base64 = base64.b64decode(base64_authorization_header)
        except (TypeError, ValueError):
            return None

        return valid_base64.decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password from the
        Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        decode_base = decoded_base64_authorization_header.split(':')

        return decode_base[0], decode_base[1]
