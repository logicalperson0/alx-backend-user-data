#!/usr/bin/env python3
""" Module of session_exp_auth views
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


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
        if session_id not in self.user_id_by_session_id.keys():
            return None

        sess_user = self.user_id_by_session_id.get(session_id)
        sess_userid = sess_user.get('user_id')
        if self.session_duration <= 0:
            return sess_userid

        cr_time = sess_user.get('created_at')
        if cr_time is None:
            return None

        ex_time = cr_time + timedelta(seconds=self.session_duration)
        if ex_time < datetime.now():
            return None
        return sess_userid
