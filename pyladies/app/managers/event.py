import json
from datetime import datetime, timedelta

from flask import current_app

from app.sqldb import DBWrapper
from .abstract import BaseEventManager
from ..utils import HashableDict

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

    @staticmethod
    def search_events(keyword, date, sort, order):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)

            events = []

            # filter events by (event title or topic name) and event date
            event_basics = manager.search_event_basics(keyword, date)

            # prepare event data
            for event_basic in event_basics:
                topic = {
                    "name": event_basic.topic.name,
                    # "desc": event_basic.topic.desc,
                    "level": event_basic.topic.level,
                    # "host": event_basic.topic.host,
                    # "freq": event_basic.topic.freq,
                    # "fields": event_basic.topic.fields,
                    "id": event_basic.topic_sn,
                }

                place_info = None
                if event_basic.place:
                    place_info = {
                        "name": event_basic.place.name,
                        # "addr": event_basic.place.addr,
                        # "map": event_basic.place.map
                    }

                event = {
                    "id": event_basic.sn,
                    "title": event_basic.event_info.title,
                    "date": event_basic.date,
                    "start_time": event_basic.start_time,
                    "end_time": event_basic.end_time,
                    # "desc": event_basic.event_info.desc,
                    "field": event_basic.event_info.fields,
                    "weekday": Manager._get_weekday(event_basic.date),
                    "time": Manager._get_time(event_basic.start_time),
                    "status": Manager._get_status(event_basic.date, event_basic.start_time),
                    "place_info": place_info,
                }

                events.append({
                    "event": event,
                    "topic": topic,
                })

            # sort events
            events = sorted(events, key=lambda x: x["event"][sort], reverse=(order == "desc"))
            return events

    @staticmethod
    def _get_weekday(event_date):
        """get event weeekday"""
        date = datetime.strptime(event_date, '%Y-%m-%d')
        return date.isoweekday() % 7

    @staticmethod
    def _get_time(event_start_time):
        """get event time"""
        hour = datetime.strptime(event_start_time, '%H:%M').hour
        if hour < 12:
            return 0
        if hour < 17:
            return 1
        return 2

    @staticmethod
    def _get_status(event_date, event_start_time):
        """get event status"""
        event_time = datetime.strptime(f'{event_date} {event_start_time}', '%Y-%m-%d %H:%M')
        current_time = datetime.utcnow() + timedelta(hours=8)
        if current_time >= event_time:
            return 0
        return 1

    @staticmethod
    def get_event(e_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_basic = manager.get_event_basic(e_id)

            place_info = None
            if event_basic.place:
                place_info = {
                    "name": event_basic.place.name,
                    "addr": event_basic.place.addr,
                    "map": event_basic.place.map
                }

            title = None
            fields = []
            desc = None
            speakers = set()
            assistants = set()
            slides = set()
            resources = set()
            if event_basic.event_info:
                title = event_basic.event_info.title
                fields = event_basic.event_info.fields
                desc = event_basic.event_info.desc
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
                "topic_info": {
                    "name": event_basic.topic.name,
                    "id": event_basic.topic.sn
                },
                "title": title,
                "fields": fields,
                "desc": desc,
                "level": event_basic.topic.level,
                "date": event_basic.date,
                "start_time": event_basic.start_time,
                "end_time": event_basic.end_time,
                "place_info": place_info,
                "host": event_basic.topic.host,
                "speakers": list(speakers),
                "assistants": list(assistants),
                "slides": list(slides),
                "resources": list(resources)
            }
            return data

    @staticmethod
    def get_events_from_distinct_topics(limit=4):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_basics = manager.get_events_from_distinct_topics(limit)
            events = []
            for event_basic in event_basics:
                if event_basic.event_info:
                    info_event = {
                        "topic_info": {
                            "name": event_basic.topic.name,
                            "id": event_basic.topic.sn,
                        },
                        "event_info": {
                            "title": event_basic.event_info.title,
                            "level": event_basic.topic.level,
                            "date": event_basic.date,
                            "start_time": event_basic.start_time,
                            "end_time": event_basic.end_time,
                            "event_basic_id": event_basic.sn
                        }
                    }
                    events.append(info_event)
            return events
