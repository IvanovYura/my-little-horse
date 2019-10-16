from flask import Flask
from flask_basicauth import BasicAuth

from service.models import User


def _check_credentials(username: str, password: str) -> bool:
    """
    Verifies given username and password for DB user
    """
    user = User(username)
    return user.verify_password(password) and user.is_admin


def init_basic_auth(app: Flask):
    basic_auth = BasicAuth(app)
    # change credential checking logic to use user from DB
    basic_auth.check_credentials = _check_credentials
