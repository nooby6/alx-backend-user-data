#!/usr/bin/env python3
"""Flask server"""

from flask import Flask, abort, jsonify, request, redirect, url_for

from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def welcome():
    """Returns a welcome message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Endpoint for registering a new user"""
    email = request.form.get("email")
    pwd = request.form.get("password")
    try:
        user = AUTH.register_user(email, pwd)
        if user:
            return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Creates a new session for the user"""
    email = request.form.get("email")
    pwd = request.form.get("password")
    if AUTH.valid_login(email, pwd):
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Resets a user's session, logging them out"""
    sess = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for("welcome"))


@app.route("/profile", methods=["GET"])
def profile():
    """Returns a logged in user's profile(email)"""
    sess = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess)
    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Endpoint for getting a user password reset token"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Endpoint for updating a user password.

    Requires the form fields: "email", "reset_token", "new_password"
    """
    email = request.form.get("email")
    token = request.form.get("reset_token")
    pwd = request.form.get("new_password")
    try:
        AUTH.update_password(token, pwd)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
    