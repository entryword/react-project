
from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseApplyManager


# TODO: error handling & input verification
class Manager(BaseApplyManager):
    @staticmethod
    def create_event_apply_info(event_apply_info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            apply_info_list = []
            for apply_info in event_apply_info["apply"]:
                input_apply_info = {
                    "channel": apply_info["channel"],
                    "type": apply_info["type"],
                    "price_default": apply_info["price"]["default"],
                    "price_student": apply_info["price"]["student"],
                    "url": apply_info["url"],
                    "qualification": apply_info["qualification"]
                }
                apply_info_list.append(str(manager.create_apply_info(input_apply_info, autocommit=True)))

            event_apply = {
                "event_basic_sn": event_apply_info["event_basic_id"],
                "apply_info_sn_list": ','.join(apply_info_list),
                "host": event_apply_info["host"],
                "start_time": event_apply_info["start_time"],
                "end_time": event_apply_info["end_time"],
                "limit_gender": event_apply_info["limit"]["gender"],
                "limit_age": event_apply_info["limit"]["age"],
                "limit_desc": event_apply_info["limit_desc"]
            }
            manager.create_event_apply(event_apply, autocommit=True)

    @staticmethod
    def update_event_apply_info(event_basic_id, event_apply_info):
        pass

    @staticmethod
    def delete_event_apply_info(event_basic_id):
        pass

    @staticmethod
    def get_event_apply_info(event_basic_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            # Get data from table event_apply and apply info
            model_event_apply_info = manager.get_event_apply_by_event_basic(event_basic_id)
            event_apply_info = {
                "event_basic_id": model_event_apply_info.event_basic_sn,
                "host": model_event_apply_info.host,
                "start_time": model_event_apply_info.start_time,
                "end_time": model_event_apply_info.end_time,
                "apply": [],
                "limit": {
                    "gender": model_event_apply_info.limit_gender,
                    "age": model_event_apply_info.limit_age
                },
                "limit_desc": model_event_apply_info.limit_desc
            }
            for apply_info_sn in model_event_apply_info.apply_info_sn_list.split(","):
                model_apply_info = manager.get_apply_info(int(apply_info_sn))
                apply_info = {
                    "channel": model_apply_info.channel,
                    "type": model_apply_info.type,
                    "price": {
                        "default": model_apply_info.price_default,
                        "student": model_apply_info.price_student
                    },
                    "url": model_apply_info.url,
                    "qualification": model_apply_info.qualification
                }
                event_apply_info["apply"].append(apply_info)
            return event_apply_info
