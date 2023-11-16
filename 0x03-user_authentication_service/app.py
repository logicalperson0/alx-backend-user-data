#!/usr/bin/env python3
"""
flask app module
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth
from user import User


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    """
    GET /
    Return:
      - JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """implements the POST /users route"""
    email = request.form.get('email')
    pwd = request.form.get('password')

    try:
        new_user = AUTH.register_user(email, pwd)
        return jsonify({"email": "{}".format(email),
                        "message": "user created"})

    except exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """return a JSON payload of the form"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not AUTH.valid_login(email, pwd):
        abort(401)
    new_sess = AUTH.create_session(email)
    if not new_sess:
        abort(401)

    res = make_response(jsonify({"email": email, "message": "logged in"}))
    res.set_cookie('session_id', new_sess)
    return res


@app.route('/sessions', methods=['DELETE'])
def logout():
    """respond to the DELETE /sessions route"""
    sess_id = request.cookies.get('session_id')

    out_user = AUTH.get_user_from_session_id(sess_id)
    if out_user is None:
        abort(403)
    AUTH.destroy_session(out_user)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
