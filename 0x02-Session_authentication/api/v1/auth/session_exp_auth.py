#!/usr/bin/env python3
""" Module of session_exp_auth views
"""
from api.v1.auth.session_auth import SessionAuth
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """creating a new exp authentication mechanism"""
    def __init__(self):
        """init method of the class"""
        sess_duration = os.getenv('SESSION_DURATION')
        try:
            session_dur = int(sess_duration)
        except Exception:
            session_dur = 0

        self.session_duration = session_dur

    def create_session(self, user_id=None):
        """will call the create_session() method of SessionAuth"""
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None

        session_dictionary = {'user_id': user_id,
                              'created_at': datetime.now()}
        self.user_id_by_session_id[sess_id] = session_dictionary

        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """return user_id from the session dictionary"""
        if session_id is None:
            return None
        if session_id not in user_id_by_session_id.keys():
            return None
        if self.session_duration is <= 0:
            return self.user_id_by_session_id.get(session_id).get('user_id')

        cr_time = self.user_id_by_session_id.get(session_id).get('created_at')
        if cr_time is None:
            return None

        if (cr_time + self.session_duration) < datetime.now():
            return None

        ex_time = cr_time + timedelta(seconds=self.session_duration)
        if ex_time < datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get('user_id')
