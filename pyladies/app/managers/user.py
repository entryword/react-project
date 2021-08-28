from flask import current_app
from flask_login import login_user, logout_user

from app.exceptions import (
    PyLadiesException,
    USER_NOT_EXIST, USER_LOGIN_FAILED,
)
from app.sqldb import DBWrapper
from .abstract import BaseUserManager


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

    @staticmethod
    def get_all_users():
        '''
        return list of users
        e.g., [
            {
                'name': 'test_name',
                'roles':[
                    {'name': 'r1', 'id': 1},
                    {'name': 'r2', 'id': 2}
                ],
                'status': 0,
                'id': 123
            },
        ]
        '''
        user_list = []
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            try:
                query_res = manager.get_all_users()
                for user in query_res:
                    user_info = {
                        'name': user.name,
                        'status': user.status,
                        'id': user.id,
                        'roles': [{'name': r.name, 'id': r.id} for r in user.roles],
                    }
                    user_list.append(user_info)
            except PyLadiesException as e:
                raise e
        return user_list
