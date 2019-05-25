import json

from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseTopicManager
from ..utils import HashableDict


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

    @staticmethod
    def get_topic(t_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            topic = manager.get_topic(t_id)

            events = []
            speakers = set()
            assistants = set()
            slides = set()
            resources = set()
            for event_basic in topic.event_basics:
                place_info = None
                if event_basic.place:
                    place_info = {
                        "name": event_basic.place.name,
                        "addr": event_basic.place.addr,
                        "map": event_basic.place.map
                    }

                events.append({
                    "id": event_basic.sn,
                    "date": event_basic.date,
                    "place_info": place_info
                })
                if event_basic.event_info:
                    events[-1]["title"] = event_basic.event_info.title
                    if event_basic.event_info.speakers:
                        for speaker in event_basic.event_info.speakers:
                            speaker_info = HashableDict({
                                "id": speaker.sn,
                                "name": speaker.name,
                                "photo": speaker.photo
                            })
                            speakers.add(speaker_info)
                    if event_basic.event_info.assistants:
                        for assistant in event_basic.event_info.assistants:
                            assistant_info = HashableDict({
                                "id": assistant.sn,
                                "name": assistant.name,
                                "photo": assistant.photo
                            })
                            assistants.add(assistant_info)
                    if event_basic.event_info.slide_resources:
                        for data in event_basic.event_info.slide_resources:
                            if data.type == "slide":
                                slide_info = HashableDict({
                                    "id": data.sn,
                                    "title": data.title,
                                    "url": data.url
                                    })
                                slides.add(slide_info)
                            else:
                                resource_info = HashableDict({
                                    "id": data.sn,
                                    "title": data.title,
                                    "url": data.url
                                    })
                                resources.add(resource_info)

            slides = sorted(slides, key=lambda x: x["id"])
            for slide in slides:
                del slide["id"]
            resources = sorted(resources, key=lambda x: x["id"])
            for resource in resources:
                del resource["id"]

            data = {
                "name": topic.name,
                "fields": topic.fields,
                "freq": topic.freq,
                "desc": topic.desc,
                "level": topic.level,
                "events": events,
                "host": topic.host,
                "speakers": list(speakers),
                "assistants": list(assistants),
                "slides": list(slides),
                "resources": list(resources)
            }
            return data

    @staticmethod
    def get_topics():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            topics = manager.get_topics()
            all_data = []
            for topic in topics:
                data = {
                    "id": topic.sn,
                    "name": topic.name
                }
                all_data.append(data)
        return all_data