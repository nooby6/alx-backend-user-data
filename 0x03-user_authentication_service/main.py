#!/usr/bin/env python3
"""Integration test for the user authentication API"""

import requests

API = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Tests POST /users"""
    form_data = {"email": email, "password": password}
    r = requests.post(f"{API}/users", data=form_data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests POST /sessions
    - wrong password
    """
    form_data = {"email": email, "password": password}
    r = requests.post(f"{API}/sessions", data=form_data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests POST /sessions
    - correct credentials
    """
    form_data = {"email": email, "password": password}
    r = requests.post(f"{API}/sessions", data=form_data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "logged in"}
    session_id = r.cookies["session_id"]
    assert isinstance(session_id, str)
    return session_id


def profile_unlogged() -> None:
    """Tests /GET profile
    - no session_id
    """
    r = requests.get(f"{API}/profile")
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests /GET profile
    - correct session token
    """
    cookie = {"session_id": session_id}
    r = requests.get(f"{API}/profile", cookies=cookie)
    assert r.status_code == 200
    assert isinstance(r.json().get("email"), str)


def log_out(session_id: str) -> None:
    """Tests DELETE /sessions
    - correct session token
    """
    cookie = {"session_id": session_id}
    r = requests.delete(f"{API}/sessions", cookies=cookie)
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Tests /POST reset_password"""
    form_data = {"email": email}
    r = requests.post(f"{API}/reset_password", data=form_data)
    assert r.status_code == 200
    resp = r.json()
    assert resp.get("email") == email
    token = resp.get("reset_token")
    assert token
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests /PUT reset_password"""
    form_data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    r = requests.put(f"{API}/reset_password", data=form_data)
    assert r.status_code == 200
    assert r.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
    