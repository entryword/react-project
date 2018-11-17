import json

from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseEventManager


# TODO: error handling & input verification
class Manager(BaseEventManager):
    @staticmethod
    def create_event(file_path):
        with open(file_path) as f:
            info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.create_event_basic(info["event_basic"], autocommit=True)
            event_basics = manager.get_event_basics_by_topic(info["event_basic"]["topic_sn"])
            for i in event_basics:
                if i.date == info["event_basic"]["date"] \
                        and i.start_time == info["event_basic"]["start_time"] \
                        and i.end_time == info["event_basic"]["end_time"]:
                    event_basic = i
                    break

            if info["event_info"]:
                info["event_info"]["event_basic_sn"] = event_basic.sn
                manager.create_event_info(info["event_info"], autocommit=True)

            return event_basic.sn

    @staticmethod
    def update_event(sn, file_path):
        with open(file_path) as f:
            new_info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            if new_info["event_basic"]:
                manager.update_event_basic(sn, new_info["event_basic"], autocommit=True)

            if new_info["event_info"]:
                event_basic = manager.get_event_basic(sn)
                if event_basic.event_info:
                    manager.update_event_info(event_basic.event_info.sn, new_info["event_info"],
                                              autocommit=True)
                else:
                    new_info["event_info"]["event_basic_sn"] = event_basic.sn
                    manager.create_event_info(new_info["event_info"], autocommit=True)

    @staticmethod
    def delete_event(sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_event_basic(sn, autocommit=True)

    @staticmethod
    def list_events(topic_sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_basics = manager.get_event_basics_by_topic(topic_sn)
            for i in event_basics:
                print(i)
                if i.event_info:
                    print(i.event_info)
