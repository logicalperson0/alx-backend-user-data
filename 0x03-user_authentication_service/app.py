#!/usr/bin/env python3
"""
flask app module
"""
from flask import Flask, jsonify, request, abort, response
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

    try:
        new_sess = AUTH.create_session(email)

        res = jsonify({"email": "{}".format(email), "message": "logged in"})
        res.set_cookie('session_id', new_sess)
        return res
    except NoResultFound:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
