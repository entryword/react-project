import json

from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseSpeakerManager


# TODO: error handling & input verification
class Manager(BaseSpeakerManager):
    @staticmethod
    def create_speaker(file_path):
        with open(file_path) as f:
            info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.create_speaker(info, autocommit=True)
            speaker = manager.get_speaker_by_name(info["name"])
            return speaker.sn

    @staticmethod
    def update_speaker(sn, file_path):
        with open(file_path) as f:
            new_info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_speaker(sn, new_info, autocommit=True)

    @staticmethod
    def delete_speaker(sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_speaker(sn, autocommit=True)

    @staticmethod
    def list_speakers():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            speakers = manager.get_speakers()
            for i in speakers:
                print(i)

    @staticmethod
    def get_speakers():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            speakers = manager.get_speakers()

            speaker_list = []
            for speaker in speakers:
                data = {
                    "id": speaker.sn,
                    "name": speaker.name,
                }
                speaker_list.append(data)
            return speaker_list

    @staticmethod
    def search_speakers(keyword, fields):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            speakers = manager.search_speakers(keyword)

            speaker_list = []
            for speaker in speakers:
                if (not fields) or (fields.intersection(set(speaker.fields))):
                    speaker_list.append({
                        "id": speaker.sn,
                        "name": speaker.name,
                        "photo": speaker.photo,
                        "title": speaker.title,
                        "fields": speaker.fields
                    })
            return speaker_list

    @staticmethod
    def get_speaker_profile(sn):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            speaker = manager.get_speaker(sn)
            links = [{"type": link.type, "url": link.url} for link in speaker.links]
            events = sorted(speaker.event_infos, key=lambda e: e.sn)
            topics = sorted(set(map(lambda e: e.event_basic.topic, events)), key=lambda t: t.sn)
            talks = [
                {
                    "topic_id": topic.sn,
                    "topic_name": topic.name,
                    "events": [
                        {"title": event.title, "id": event.sn}
                        for event in events if event.event_basic.topic.sn == topic.sn
                    ]
                } for topic in topics
            ]

            data = {
                "name": speaker.name,
                "photo": speaker.photo,
                "title": speaker.title,
                "major_related": speaker.major_related,
                "intro": speaker.intro,
                "fields": speaker.fields,
                "links": links,
                "talks": talks
            }
            return data
