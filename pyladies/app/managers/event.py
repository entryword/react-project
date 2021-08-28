import json
from datetime import datetime, timedelta

from flask import current_app

from app.exceptions import PyLadiesException, APPLY_NOT_EXIST
from app.managers.apply import Manager as ApplyManager
from app.sqldb import DBWrapper
from .abstract import BaseEventManager
from ..utils import HashableDict


# TODO: error handling & input verification
class Manager(BaseEventManager):
    @staticmethod
    def create_event(info):
        if not isinstance(info, dict):
            with open(info) as f:
                info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_basic_id = manager.create_event_basic(info["event_basic"], autocommit=True)

            if info["event_info"]:
                info["event_info"]["event_basic_id"] = event_basic_id
                manager.create_event_info(info["event_info"], autocommit=True)

            return event_basic_id

    @staticmethod
    def update_event(id, new_info):
        if not isinstance(new_info, dict):
            with open(new_info) as f:
                new_info = json.loads(f.read())

        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            if new_info["event_basic"]:
                manager.update_event_basic(id, new_info["event_basic"], autocommit=True)

            event_basic = manager.get_event_basic(id)
            if new_info["event_info"]:
                if event_basic.event_info:
                    manager.update_event_info(event_basic.event_info.id, new_info["event_info"],
                                              autocommit=True)
                else:
                    new_info["event_info"]["event_basic_id"] = event_basic.id
                    manager.create_event_info(new_info["event_info"], autocommit=True)

            if "apply_info" in new_info and new_info["apply_info"]:
                new_info["apply_info"]["event_basic_id"] = event_basic.id
                if event_basic.apply:
                    manager.update_event_apply(event_basic.apply.id, new_info["apply_info"], autocommit=True)
                else:
                    manager.create_event_apply(new_info["apply_info"], autocommit=True)

    @staticmethod
    def delete_event(id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            manager.delete_event_basic(id, autocommit=True)

    @staticmethod
    def list_events(topic_id):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_basics = manager.get_event_basics_by_topic(topic_id)
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
                    "id": event_basic.topic_id,
                }

                place_info = None
                if event_basic.place:
                    place_info = {
                        "name": event_basic.place.name,
                        # "addr": event_basic.place.addr,
                        # "map": event_basic.place.map
                    }

                event = {
                    "id": event_basic.id,
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
        event_time = datetime.strptime(
            '{} {}'.format(event_date, event_start_time), '%Y-%m-%d %H:%M')
        current_time = datetime.utcnow() + timedelta(hours=8)
        if current_time >= event_time:
            return 0
        return 1

    @staticmethod
    def get_event(e_id, apimode=None):
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_basic = manager.get_event_basic(e_id)
            try:
                tm = ApplyManager()
                event_apply_info = tm.get_event_apply_info_by_event_basic_id(e_id)
                event_apply_info = event_apply_info["apply"]
            except PyLadiesException as e:
                if e.code == APPLY_NOT_EXIST.code:
                    event_apply_info = None
                else:
                    raise

            place_info = None
            if event_basic.place:
                place_info = {
                    "id": event_basic.place.id,
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
                            "id": speaker.id,
                            "name": speaker.name,
                            "photo": speaker.photo
                        })
                        speakers.add(speaker_info)
                if event_basic.event_info.assistants:
                    for assistant in event_basic.event_info.assistants:
                        assistant_info = HashableDict({
                            "id": assistant.id,
                            "name": assistant.name,
                            "photo": assistant.photo
                        })
                        assistants.add(assistant_info)
                if event_basic.event_info.slide_resources:
                    for data in event_basic.event_info.slide_resources:
                        if data.type == "slide":
                            slide_info = HashableDict({
                                "id": data.id,
                                "title": data.title,
                                "url": data.url
                                })
                            slides.add(slide_info)
                        else:
                            resource_info = HashableDict({
                                "id": data.id,
                                "title": data.title,
                                "url": data.url
                                })
                            resources.add(resource_info)

            slides = sorted(slides, key=lambda x: x["id"])
            resources = sorted(resources, key=lambda x: x["id"])

            data = {
                "topic_info": {
                    "name": event_basic.topic.name,
                    "id": event_basic.topic.id
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
            
            if apimode:
                data["topic_id"] = data["topic_info"]["id"]
                data["start_date"] = data["date"]
                # TODO:waiting table schema and data["end_date"] will add here
                data["end_date"] = data["date"]
                if data.get("topic_info"): del data["topic_info"]
                if data.get("date"): del data["date"]
                if data["place_info"].get("addr"): del data["place_info"]["addr"]
                if data["place_info"].get("map"): del data["place_info"]["map"]
                for ind, sp in enumerate(data["speakers"]):
                    if sp.get("photo"): del data["speakers"][ind]["photo"]
                for ind, sp in enumerate(data["assistants"]):
                    if sp.get("photo"): del data["assistants"][ind]["photo"] 
                for ind, sp in enumerate(data["slides"]):
                    if sp.get("photo"): del data["slides"][ind]["photo"]
                for ind, sp in enumerate(data["resources"]):
                    if sp.get("photo"): del data["resources"][ind]["photo"]  
                data["slide_resources"] = data["slides"] + data["resources"]
                if event_apply_info:
                    data["apply"] = event_apply_info
                else:
                    data["apply"] = []
            else:
                del data["place_info"]["id"]
                for ind, sp in enumerate(data["slides"]):
                    if sp.get("id"): del data["slides"][ind]["id"]
                for ind, sp in enumerate(data["resources"]):
                    if sp.get("id"): del data["resources"][ind]["id"]

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
                            "id": event_basic.topic.id,
                        },
                        "event_info": {
                            "title": event_basic.event_info.title,
                            "level": event_basic.topic.level,
                            "date": event_basic.date,
                            "start_time": event_basic.start_time,
                            "end_time": event_basic.end_time,
                            "event_basic_id": event_basic.id
                        }
                    }
                    events.append(info_event)
            return events

    @staticmethod
    def get_events():
        with DBWrapper(current_app.db.engine.url).session() as db_sess:
            manager = current_app.db_api_class(db_sess)
            event_basics = manager.get_event_basics()
            events = []
            for event_basic in event_basics:
                data = {
                    "id": event_basic.id,
                    "title": event_basic.event_info.title,
                    "topic": {
                        "name": event_basic.topic.name
                    },
                    "place": {
                        "name": event_basic.place.name
                    },
                    "date": event_basic.date,
                    "start_time": event_basic.start_time,
                    "end_time": event_basic.end_time
                }
                if event_basic.apply and event_basic.apply.apply:
                    data["event_apply_exist"] = 1
                else:
                    data["event_apply_exist"] = 0

                if event_basic.event_info.speakers:
                    data["speaker_exist"] = 1
                else:
                    data["speaker_exist"] = 0

                events.append(data)
            return events
