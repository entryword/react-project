import json

from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseTopicManager


# TODO: error handling & input verification
class Manager(BaseTopicManager):
    @staticmethod
    def create_topic(file_path):
        with open(file_path) as f:
            info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)
            topic = manager.get_topic_by_name(info["name"])
            return topic.sn

    @staticmethod
    def update_topic(sn, file_path):
        with open(file_path) as f:
            new_info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_topic(sn, new_info, autocommit=True)

    @staticmethod
    def delete_topic(sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_topic(sn, autocommit=True)

    @staticmethod
    def list_topics(key=None):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            if key is None:
                topics = manager.get_topics()
                for i in topics:
                    print(i)
            else:
                topics = manager.get_topics_by_keyword(key)
                for i in topics:
                    print(i)
