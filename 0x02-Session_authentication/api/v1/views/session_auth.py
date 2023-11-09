#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
import os
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      create a Session ID for the User ID
    """
    email = request.form.get('email')
    # pwd = request.form.get('password')

    if not email or email == '':
        return make_response(jsonify({'error': 'email missing'}), 400)

    pwd = request.form.get('password')
    if not pwd or pwd == '':
        return make_response(jsonify({'error': 'password missing'}), 400)

    user_em = User.search({'email': email})
    if len(user_em) == 0:
        return make_response(jsonify({'error': 'no user found\
                             for this email'}), 404)

    from api.v1.app import auth
    for u in user_em:
        if u.is_valid_password(pwd):
            sess_id = auth.create_session(u.id)
            SESSION_NAME = os.getenv('SESSION_NAME')
            response = make_response(jsonify({}))
            response.set_cookie(SESSION_NAME, sess_id)

            return response

    return make_response(jsonify({'error': 'wrong password'}), 401)
