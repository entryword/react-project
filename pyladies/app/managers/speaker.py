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
            return speaker.id

    @staticmethod
    def create_speaker_by_object(speaker_info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.create_speaker(speaker_info, autocommit=True)
            speaker = manager.get_speaker_by_name(speaker_info["name"])
            return speaker.id

    @staticmethod
    def update_speaker(id, file_path):
        with open(file_path) as f:
            new_info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_speaker(id, new_info, autocommit=True)

    @staticmethod
    def update_speaker_by_object(id, speaker_info):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.update_speaker(id, speaker_info, autocommit=True)

    @staticmethod
    def delete_speaker(id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_speaker(id, autocommit=True)

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
                    "id": speaker.id,
                    "name": speaker.name,
                    "title": speaker.title
                }
                speaker_list.append(data)
            return speaker_list

    @staticmethod
    def get_speaker(speaker_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            speaker = manager.get_speaker(speaker_id)
            links = [{"type": link.type, "url": link.url} for link in speaker.links]
            data = {
                "name": speaker.name,
                "photo": speaker.photo,
                "title": speaker.title,
                "major_related": speaker.major_related,
                "intro": speaker.intro,
                "fields": speaker.fields,
                "links": links
            }
            return data

    @staticmethod
    def search_speakers(keyword, fields):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            speakers = manager.search_speakers(keyword)

            speaker_list = []
            for speaker in speakers:
                if (not fields) or (fields.intersection(set(speaker.fields))):
                    speaker_list.append({
                        "id": speaker.id,
                        "name": speaker.name,
                        "photo": speaker.photo,
                        "title": speaker.title,
                        "fields": speaker.fields
                    })
            return speaker_list

    @staticmethod
    def get_speaker_profile(id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            speaker = manager.get_speaker(id)
            links = [{"type": link.type, "url": link.url} for link in speaker.links]
            events = sorted(speaker.event_infos, key=lambda e: e.id)
            topics = sorted(set(map(lambda e: e.event_basic.topic, events)), key=lambda t: t.id)
            talks = [
                {
                    "topic_id": topic.id,
                    "topic_name": topic.name,
                    "events": [
                        {"title": event.title, "id": event.id}
                        for event in events if event.event_basic.topic.id == topic.id
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
