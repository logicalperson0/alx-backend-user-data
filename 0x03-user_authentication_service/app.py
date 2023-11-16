#!/usr/bin/env python3
"""
flask app module
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
