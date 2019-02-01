
from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseApplyManager


# TODO: error handling & input verification
class Manager(BaseApplyManager):
    @staticmethod
    def create_event_apply_info(file_path):
        pass

    @staticmethod
    def update_event_apply_info(event_basic_id, file_path):
        pass

    @staticmethod
    def delete_event_apply_info(event_basic_id):
        pass

    @staticmethod
    def get_event_apply_info(event_basic_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_apply_info = manager.get_event_apply_info_by_event_basic_id(event_basic_id)
            return event_apply_info
