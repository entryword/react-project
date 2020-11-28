from flask import current_app
from jsonschema import validate

from app.exceptions import ROLE_NAME_DUPLICATE
from app.schemas.role_info import schema_create
from app.sqldb import DBWrapper
from .abstract import BaseRoleManager


class Manager(BaseRoleManager):
    @staticmethod
    def create_role(info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            try:
                sn = manager.create_role(info, autocommit=True)
            except Exception as e:
                if "duplicate" in str(e).lower():
                    raise ROLE_NAME_DUPLICATE
                raise e
            return sn

    @staticmethod
    def update_role(role_sn, info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            try:
                manager.update_role(role_sn, info, autocommit=True)
            except Exception as e:
                if "duplicate" in str(e).lower():
                    raise ROLE_NAME_DUPLICATE
                raise e

    @staticmethod
    def delete_role(role_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_role(role_sn, autocommit=True)

    @staticmethod
    def get_role(role_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            role = manager.get_role(role_sn)
            data = {'id': role.sn, 'name': role.name, 'permission': role.permission}
            return data

    @staticmethod
    def get_roles():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            roles = manager.get_roles()
            data = [{'id': r.sn, 'name': r.name, 'permission': r.permission} for r in roles]
            return data
