from datetime import datetime

from flask import current_app
from jsonschema import validate

from app.schemas.event_apply_info import schema_create
from app.sqldb import DBWrapper
from .abstract import BaseApplyManager


# TODO: error handling & input verification
class Manager(BaseApplyManager):
    @staticmethod
    def create_event_apply_info(event_apply_info):
        validate(event_apply_info, schema_create)
        for item in event_apply_info["apply"]:
            datetime.strptime(item["start_time"], "%Y-%m-%d %H:%M")
            datetime.strptime(item["end_time"], "%Y-%m-%d %H:%M")

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            return manager.create_event_apply(event_apply_info, autocommit=True)

    @staticmethod
    def get_event_apply_info_by_event_basic_sn(event_basic_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_apply_info = manager.get_event_apply_by_event_basic_sn(event_basic_sn)
            data = {
                "event_basic_sn": event_apply_info.event_basic_sn,
                "apply": event_apply_info.apply
            }
            return data

    @staticmethod
    def get_event_apply_info(event_apply_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_apply_info = manager.get_event_apply(event_apply_sn)
            data = {
                "event_basic_sn": event_apply_info.event_basic_sn,
                "apply": event_apply_info.apply
            }
            return data

    @staticmethod
    def get_event_apply_one_or_none(event_apply_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_apply_info = manager.get_event_apply_one_or_none(event_apply_sn)
            return event_apply_info

    @staticmethod
    def update_event_apply_info(event_apply_sn, update_info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_event_apply(event_apply_sn, update_info, autocommit=True)

    @staticmethod
    def delete_event_apply_info(event_apply_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_event_apply(event_apply_sn, autocommit=True)
