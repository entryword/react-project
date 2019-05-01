import json

from flask import current_app
from flask_login import login_user, logout_user

from .abstract import BaseUserManager
from app.exceptions import (
    PyLadiesException,
    USER_NOT_EXIST, USER_LOGIN_FAILED,
)
from app.sqldb import DBWrapper


class Manager(BaseUserManager):
    @staticmethod
    def login(username, password):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            try:
                user = manager.get_user_by_name(username)
                if not user.verify_password(password):
                    raise USER_LOGIN_FAILED
                login_user(user, False)
            except PyLadiesException as e:
                if e.code == USER_NOT_EXIST.code:
                    raise USER_LOGIN_FAILED
                raise e

    @staticmethod
    def logout():
        logout_user()
