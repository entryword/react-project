from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseApplyManager


# TODO: error handling & input verification
class Manager(BaseApplyManager):
    @staticmethod
    def create_event_apply_info(event_apply_info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            return manager.create_event_apply(event_apply_info["data"], autocommit=True)

    @staticmethod
    def get_event_apply_info_by_event_basic_sn(event_basic_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_apply_info = manager.get_event_apply_by_event_basic_sn(event_basic_sn)
            return {"data": event_apply_info}

    @staticmethod
    def get_event_apply_info(event_apply_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_apply_info = manager.get_event_apply(event_apply_sn)
            return {"data": event_apply_info}

    @staticmethod
    def update_event_apply_info(event_apply_sn, update_info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_event_apply(event_apply_sn, update_info["data"], autocommit=True)

    @staticmethod
    def delete_event_apply_info(event_apply_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_event_apply(event_apply_sn, autocommit=True)
