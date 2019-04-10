# coding=UTF-8

import unittest
import json
from app import create_app
from app.sqldb import DBWrapper
from app.exceptions import (
    EVENTLIST_INVALID_KEYWORD,
    EVENTLIST_INVALID_DATE,
    EVENTLIST_INVALID_SORT,
    EVENTLIST_INVALID_ORDER,
)


class RESTfulAPIv1_0TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("test")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_routing_not_found(self):
        rv = self.test_client.get("/topic/1")
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(rv.json["info"]["code"], 8000)

    def test_topic_not_exist(self):
        rv = self.test_client.get("/v1.0/api/topic/1")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 1000)

    def test_get_topic_without_event(self):
        info = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2],
        }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/topic/1")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"]["name"], info["name"])
        self.assertEqual(rv.json["data"]["desc"], info["desc"])
        self.assertEqual(rv.json["data"]["freq"], info["freq"])
        self.assertEqual(rv.json["data"]["level"], info["level"])
        self.assertEqual(rv.json["data"]["host"], info["host"])
        self.assertEqual(rv.json["data"]["fields"], info["fields"])
        self.assertEqual(rv.json["data"]["events"], [])
        self.assertEqual(rv.json["data"]["speakers"], [])
        self.assertEqual(rv.json["data"]["assistants"], [])
        self.assertEqual(rv.json["data"]["slides"], [])

    def test_get_topic_with_event(self):
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html",
        }
        speaker_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
        }
        assistant_info = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
        }
        slide_resources = [
            {
                "type": "slide",
                "title": "Flask Web Development - class 1",
                "url": "http://tw.pyladies.com/~maomao/1_flask.slides.html#/",
            },
            {
                "type": "resource",
                "title": "Source Code",
                "url": "https://github.com/win911/flask_class",
            },
        ]
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2],
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00",
        }
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1],
            "slide_resources": slide_resources,
        }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_place(place_info, autocommit=True)
            event_basic_info["place_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info_info["event_basic_sn"] = 1
            manager.create_speaker(speaker_info, autocommit=True)
            event_info_info["speaker_sns"] = [1]
            manager.create_speaker(assistant_info, autocommit=True)
            event_info_info["assistant_sns"] = [2]
            manager.create_event_info(event_info_info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/topic/1")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]["events"]), 1)
        self.assertEqual(rv.json["data"]["events"][0]["date"], event_basic_info["date"])
        self.assertEqual(rv.json["data"]["events"][0]["place_info"]["name"], place_info["name"])
        self.assertEqual(rv.json["data"]["events"][0]["place_info"]["addr"], place_info["addr"])
        self.assertEqual(rv.json["data"]["events"][0]["place_info"]["map"], place_info["map"])
        self.assertEqual(rv.json["data"]["events"][0]["title"], event_info_info["title"])
        self.assertEqual(len(rv.json["data"]["speakers"]), 1)
        self.assertEqual(rv.json["data"]["speakers"][0]["name"], speaker_info["name"])
        self.assertEqual(rv.json["data"]["speakers"][0]["photo"], speaker_info["photo"])
        self.assertEqual(len(rv.json["data"]["assistants"]), 1)
        self.assertEqual(rv.json["data"]["assistants"][0]["name"], assistant_info["name"])
        self.assertEqual(rv.json["data"]["assistants"][0]["photo"], assistant_info["photo"])
        self.assertEqual(len(rv.json["data"]["slides"]), 1)
        self.assertEqual(rv.json["data"]["slides"][0]["title"], slide_resources[0]["title"])
        self.assertEqual(rv.json["data"]["slides"][0]["url"], slide_resources[0]["url"])
        self.assertEqual(len(rv.json["data"]["resources"]), 1)
        self.assertEqual(rv.json["data"]["resources"][0]["title"], slide_resources[1]["title"])
        self.assertEqual(rv.json["data"]["resources"][0]["url"], slide_resources[1]["url"])

    def test_get_event_not_exist(self):
        rv = self.test_client.get("/v1.0/api/event/1")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 1100)

    def test_get_event_without_details(self):
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html",
        }
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2],
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00",
        }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_place(place_info, autocommit=True)
            event_basic_info["place_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/event/1")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"]["topic_info"]["name"], topic_info["name"])
        self.assertEqual(rv.json["data"]["title"], None)
        self.assertEqual(rv.json["data"]["fields"], [])
        self.assertEqual(rv.json["data"]["desc"], None)
        self.assertEqual(rv.json["data"]["level"], topic_info["level"])
        self.assertEqual(rv.json["data"]["date"], event_basic_info["date"])
        self.assertEqual(rv.json["data"]["start_time"], event_basic_info["start_time"])
        self.assertEqual(rv.json["data"]["end_time"], event_basic_info["end_time"])
        self.assertEqual(rv.json["data"]["place_info"]["name"], place_info["name"])
        self.assertEqual(rv.json["data"]["place_info"]["addr"], place_info["addr"])
        self.assertEqual(rv.json["data"]["place_info"]["map"], place_info["map"])
        self.assertEqual(rv.json["data"]["host"], topic_info["host"])
        self.assertEqual(rv.json["data"]["speakers"], [])
        self.assertEqual(rv.json["data"]["assistants"], [])
        self.assertEqual(rv.json["data"]["slides"], [])

    def test_get_event_with_details(self):
        place_info = {
            "name": "place 1",
            "addr": "台北市信義區光復南路133號",
            "map": "http://abc.com/map.html",
        }
        speaker_info = {
            "name": "speaker 1",
            "photo": "https://pyladies.marsw.tw/img/speaker_1_photo.png",
            "title": "Senior Engineer",
            "major_related": True,
            "intro": "",
            "fields": [3],
        }
        assistant_info = {
            "name": "speaker 2",
            "photo": "https://pyladies.marsw.tw/img/speaker_2_photo.png",
            "title": "Engineer",
            "major_related": True,
            "intro": "",
            "fields": [0, 1],
        }
        slide_resources = [
            {
                "type": "slide",
                "title": "Flask Web Development - class 1",
                "url": "http://tw.pyladies.com/~maomao/1_flask.slides.html#/",
            },
            {
                "type": "resource",
                "title": "Source Code",
                "url": "https://github.com/win911/flask_class",
            },
        ]
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2],
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00",
        }
        event_info_info = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1],
            "slide_resources": slide_resources,
        }

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            event_basic_info["topic_sn"] = 1
            manager.create_place(place_info, autocommit=True)
            event_basic_info["place_sn"] = 1
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_info_info["event_basic_sn"] = 1
            manager.create_speaker(speaker_info, autocommit=True)
            event_info_info["speaker_sns"] = [1]
            manager.create_speaker(assistant_info, autocommit=True)
            event_info_info["assistant_sns"] = [2]
            manager.create_event_info(event_info_info, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/event/1")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"]["title"], event_info_info["title"])
        self.assertEqual(rv.json["data"]["fields"], event_info_info["fields"])
        self.assertEqual(rv.json["data"]["desc"], event_info_info["desc"])
        self.assertEqual(len(rv.json["data"]["speakers"]), 1)
        self.assertEqual(rv.json["data"]["speakers"][0]["name"], speaker_info["name"])
        self.assertEqual(rv.json["data"]["speakers"][0]["photo"], speaker_info["photo"])
        self.assertEqual(len(rv.json["data"]["assistants"]), 1)
        self.assertEqual(rv.json["data"]["assistants"][0]["name"], assistant_info["name"])
        self.assertEqual(rv.json["data"]["assistants"][0]["photo"], assistant_info["photo"])
        self.assertEqual(len(rv.json["data"]["slides"]), 1)
        self.assertEqual(rv.json["data"]["slides"][0]["title"], slide_resources[0]["title"])
        self.assertEqual(rv.json["data"]["slides"][0]["url"], slide_resources[0]["url"])
        self.assertEqual(len(rv.json["data"]["resources"]), 1)
        self.assertEqual(rv.json["data"]["resources"][0]["title"], slide_resources[1]["title"])
        self.assertEqual(rv.json["data"]["resources"][0]["url"], slide_resources[1]["url"])

    def test_search_events(self):
        topics = [
            {
                "name": "topic 1",
                "desc": "this is topic 1",
                "freq": 0,
                "level": 0,
                "host": 0,
                "fields": [0],
            },
            {
                "name": "topic 2",
                "desc": "this is topic 2",
                "freq": 0,
                "level": 0,
                "host": 0,
                "fields": [0],
            },
        ]
        place_info = {"name": "國立台灣大學", "addr": "台北市大安區羅斯福路四段1號", "map": ""}
        event_basics = [
            {
                "topic_sn": 1,
                "date": "2019-01-07",
                "start_time": "10:00",
                "end_time": "12:00",
                "place_sn": 1,
            },
            {
                "topic_sn": 1,
                "date": "2019-02-17",
                "start_time": "17:30",
                "end_time": "20:00",
                "place_sn": None,
            },
        ]
        event_infos = [
            {
                "event_basic_sn": 1,
                "title": "event 1",
                "desc": "this is event 1",
                "fields": [0, 1],
            },
            {
                "event_basic_sn": 2,
                "title": "event 2",
                "desc": "this is event 2",
                "fields": [0],
            },
        ]

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for topic in topics:
                manager.create_topic(topic, autocommit=True)
            manager.create_place(place_info, autocommit=True)
            for event_basic in event_basics:
                manager.create_event_basic(event_basic, autocommit=True)
            for event_info in event_infos:
                manager.create_event_info(event_info, autocommit=True)

            # test invalid keyword parameters
            rv = self.test_client.get("/v1.0/api/events?keyword=abcdefghijklmnopqrstuvwxyz12345")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], EVENTLIST_INVALID_KEYWORD.code)

            # test invalid date parameters
            rv = self.test_client.get("/v1.0/api/events?date=123")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], EVENTLIST_INVALID_DATE.code)

            # test invalid sort parameters
            rv = self.test_client.get("/v1.0/api/events?sort=123")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], EVENTLIST_INVALID_SORT.code)

            # test invalid order parameters
            rv = self.test_client.get("/v1.0/api/events?order=123")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], EVENTLIST_INVALID_ORDER.code)

            # test default parameters
            # keyword = '', date = '', sort = 'date', order='asc'
            rv = self.test_client.get("/v1.0/api/events")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], 0)
            self.assertEqual(len(rv.json["data"]["events"]), 2)
            self.assertEqual(rv.json["data"]["events"][0]["event"]["title"], "event 1")

            # test empty parameters
            rv = self.test_client.get("/v1.0/api/events?keyword=&date=&sort=&order=")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], 0)
            self.assertEqual(len(rv.json["data"]["events"]), 2)
            self.assertEqual(rv.json["data"]["events"][0]["event"]["title"], "event 1")

            # test order desc
            rv = self.test_client.get("/v1.0/api/events?order=desc")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], 0)
            self.assertEqual(len(rv.json["data"]["events"]), 2)
            self.assertEqual(rv.json["data"]["events"][0]["event"]["title"], "event 2")

            # test topic keyword with date
            rv = self.test_client.get("/v1.0/api/events?keyword=topic 1&date=2019-01")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], 0)
            self.assertEqual(len(rv.json["data"]["events"]), 1)
            self.assertEqual(rv.json["data"]["events"][0]["event"]["title"], "event 1")

            # test event keyword with date
            rv = self.test_client.get("/v1.0/api/events?keyword=event 2&date=2019-01")
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.json["info"]["code"], 0)
            self.assertEqual(len(rv.json["data"]["events"]), 0)

    def test_get_definitions(self):
        rv = self.test_client.get("/v1.0/api/definitions")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]["field"]), 12)
        self.assertEqual(len(rv.json["data"]["freq"]), 3)
        self.assertEqual(len(rv.json["data"]["level"]), 4)
        self.assertEqual(len(rv.json["data"]["host"]), 3)
        self.assertEqual(len(rv.json["data"]["status"]), 2)
        self.assertEqual(len(rv.json["data"]["weekday"]), 7)
        self.assertEqual(len(rv.json["data"]["time"]), 3)
        self.assertEqual(len(rv.json["data"]["channel"]), 2)
        self.assertEqual(len(rv.json["data"]["type"]), 2)

    def test_get_definition(self):
        rv = self.test_client.get("/v1.0/api/definition/field")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 12)

        rv = self.test_client.get("/v1.0/api/definition/freq")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 3)

        rv = self.test_client.get("/v1.0/api/definition/level")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 4)

        rv = self.test_client.get("/v1.0/api/definition/host")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 3)

        rv = self.test_client.get("/v1.0/api/definition/status")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 2)

        rv = self.test_client.get("/v1.0/api/definition/weekday")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 7)

        rv = self.test_client.get("/v1.0/api/definition/time")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 3)

        rv = self.test_client.get("/v1.0/api/definition/channel")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 2)

        rv = self.test_client.get("/v1.0/api/definition/type")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(len(rv.json["data"]), 2)

    def test_get_places(self):
        places = [
            {
                "name": "place 1",
                "addr": "台北市信義區光復南路133號",
                "map": "http://abc.com/map1.html",
            },
            {
                "name": "place 2",
                "addr": "台北市萬華區艋舺大道101號",
                "map": "http://abc.com/map2.html",
            },
            {
                "name": "place 3",
                "addr": "台北市大安區和平東路二段50號",
                "map": "http://abc.com/map3.html",
            },
        ]

        # preparation
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            manager = self.app.db_api_class(db_sess)
            for place in places:
                manager.create_place(place, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/places")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"]["places"][1]["name"], places[1]["name"])
        self.assertEqual(rv.json["data"]["places"][1]["addr"], places[1]["addr"])
        self.assertEqual(rv.json["data"]["places"][1]["map"], places[1]["map"])
        self.assertEqual(len(rv.json["data"]["places"]), 3)

    def test_get_event_apply_info(self):
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2],
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00",
        }

        apply_info_1 = {
            "host": "婦女館",
            "channel": 1,
            "type": "all",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": "一般人400元，學生200元",
            "limit": "限女",
            "url": "https://...",
            "qualification": "https://...",
        }

        apply_info_2 = {
            "host": "American Innovation Center 美國創新中心",
            "channel": 0,
            "type": "one",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": "一般人100元，學生50元",
            "limit": "限女",
            "url": "https://...",
            "qualification": "https://...",
        }

        input_event_apply = {
            "event_basic_sn": None,
            "apply": [apply_info_1, apply_info_2]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn
            event_apply_sn = manager.create_event_apply(
                input_event_apply, autocommit=True
            )

        # test
        rv = self.test_client.get("/v1.0/api/apply_info/" + str(event_apply_sn))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"], input_event_apply)

    def test_get_event_apply_info_by_event_basic_sn(self):
        topic_info = {
            "name": "Flask",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2],
        }
        event_basic_info = {
            "topic_sn": None,
            "date": "2017-01-01",
            "start_time": "14:00",
            "end_time": "16:00",
        }

        apply_info_1 = {
            "host": "婦女館",
            "channel": 1,
            "type": "all",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": "一般人400元，學生200元",
            "limit": "限女",
            "url": "https://...",
            "qualification": "https://...",
        }

        apply_info_2 = {
            "host": "American Innovation Center 美國創新中心",
            "channel": 0,
            "type": "one",
            "start_time": "2019-11-23 08:00",
            "end_time": "2019-12-01 23:00",
            "price": "一般人100元，學生50元",
            "limit": "限女",
            "url": "https://...",
            "qualification": "https://...",
        }

        input_event_apply = {
            "event_basic_sn": None,
            "apply": [apply_info_1, apply_info_2]
        }

        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)
            manager.create_topic(topic_info, autocommit=True)
            topic = manager.get_topic_by_name(topic_info["name"])
            event_basic_info["topic_sn"] = topic.sn
            manager.create_event_basic(event_basic_info, autocommit=True)
            event_basic = topic.event_basics[0]
            input_event_apply["event_basic_sn"] = event_basic.sn
            manager.create_event_apply(input_event_apply, autocommit=True)

        # test
        rv = self.test_client.get("/v1.0/api/event/"
                                  + str(input_event_apply["event_basic_sn"]) + "/apply_info")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        self.assertEqual(rv.json["data"], input_event_apply)

    def test_get_event_apply_info_but_event_not_exist(self):
        rv = self.test_client.get("/v1.0/api/apply_info/0")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 1600)

    def test_get_event_apply_info_by_event_basic_sn_but_event_not_exist(self):
        rv = self.test_client.get("/v1.0/api/event/0/apply_info")
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 1600)

    def test_get_events_from_distinct_topics(self):
        topic_info_1 = {
            "name": "topic 1",
            "desc": "This is description",
            "freq": 0,
            "level": 1,
            "host": 0,
            "fields": [0, 1, 2],
        }
        topic_info_2 = {
            "name": "topic 2",
            "desc": "This is description",
            "freq": 0,
            "level": 2,
            "host": 0,
            "fields": [0, 1, 2],
        }
        topic_info_3 = {
            "name": "topic 3",
            "desc": "This is description",
            "freq": 0,
            "level": 3,
            "host": 0,
            "fields": [0, 1, 2],
        }
        topic_info_4 = {
            "name": "topic 4",
            "desc": "This is description",
            "freq": 0,
            "level": 4,
            "host": 0,
            "fields": [0, 1, 2],
        }
        event_basic_info_1 = {
            "topic_sn": None,
            "date": "2020-01-01",
            "start_time": "14:00",
            "end_time": "16:00",
        }
        event_basic_info_2 = {
            "topic_sn": None,
            "date": "2020-03-08",
            "start_time": "14:00",
            "end_time": "16:00",
        }
        event_basic_info_3 = {
            "topic_sn": None,
            "date": "2020-05-25",
            "start_time": "14:00",
            "end_time": "16:00",
        }
        event_basic_info_4 = {
            "topic_sn": None,
            "date": "2020-10-30",
            "start_time": "14:00",
            "end_time": "16:00",
        }

        event_info_1 = {
            "event_basic_sn": None,
            "title": "Flask class 1",
            "desc": "This is description of class 1",
            "fields": [0, 1],
        }
        event_info_2 = {
            "event_basic_sn": None,
            "title": "Flask class 2",
            "desc": "This is description of class 2",
            "fields": [0, 1],
        }
        event_info_3 = {
            "event_basic_sn": None,
            "title": "Flask class 3",
            "desc": "This is description of class 3",
            "fields": [0, 1],
        }
        event_info_4 = {
            "event_basic_sn": None,
            "title": "Flask class 4",
            "desc": "This is description of class 4",
            "fields": [0, 1],
        }
        with DBWrapper(self.app.db.engine.url).session() as db_sess:
            # preparation
            manager = self.app.db_api_class(db_sess)

            topic_1 = manager.create_topic(topic_info_1, autocommit=True)
            topic_2 = manager.create_topic(topic_info_2, autocommit=True)
            topic_3 = manager.create_topic(topic_info_3, autocommit=True)
            topic_4 = manager.create_topic(topic_info_4, autocommit=True)

            event_basic_info_1["topic_sn"] = topic_1
            event_basic_info_2["topic_sn"] = topic_2
            event_basic_info_3["topic_sn"] = topic_3
            event_basic_info_4["topic_sn"] = topic_4

            event_basic_1_id = manager.create_event_basic(
                event_basic_info_1, autocommit=True
            )
            event_basic_2_id = manager.create_event_basic(
                event_basic_info_2, autocommit=True
            )
            event_basic_3_id = manager.create_event_basic(
                event_basic_info_3, autocommit=True
            )
            event_basic_4_id = manager.create_event_basic(
                event_basic_info_4, autocommit=True
            )

            event_info_1["event_basic_sn"] = event_basic_1_id
            event_info_2["event_basic_sn"] = event_basic_2_id
            event_info_3["event_basic_sn"] = event_basic_3_id
            event_info_4["event_basic_sn"] = event_basic_4_id

            manager.create_event_info(event_info_1, autocommit=True)
            manager.create_event_info(event_info_2, autocommit=True)
            manager.create_event_info(event_info_3, autocommit=True)
            manager.create_event_info(event_info_4, autocommit=True)

        # test ＆ assertion
        rv = self.test_client.get("/v1.0/api/events_from_distinct_topics")

        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.json["info"]["code"], 0)
        ans_1 = {
            "topic_info": {"name": topic_info_1["name"], "id": topic_1},
            "event_info": {
                "title": event_info_1["title"],
                "level": topic_info_1["level"],
                "date": event_basic_info_1["date"],
                "start_time": event_basic_info_1["start_time"],
                "end_time": event_basic_info_1["end_time"],
                "event_basic_id": event_basic_1_id,
            },
        }
        ans_2 = {
            "topic_info": {"name": topic_info_2["name"], "id": topic_2},
            "event_info": {
                "title": event_info_2["title"],
                "level": topic_info_2["level"],
                "date": event_basic_info_2["date"],
                "start_time": event_basic_info_2["start_time"],
                "end_time": event_basic_info_2["end_time"],
                "event_basic_id": event_basic_2_id,
            },
        }
        ans_3 = {
            "topic_info": {"name": topic_info_3["name"], "id": topic_3},
            "event_info": {
                "title": event_info_3["title"],
                "level": topic_info_3["level"],
                "date": event_basic_info_3["date"],
                "start_time": event_basic_info_3["start_time"],
                "end_time": event_basic_info_3["end_time"],
                "event_basic_id": event_basic_3_id,
            },
        }
        ans_4 = {
            "topic_info": {"name": topic_info_4["name"], "id": topic_4},
            "event_info": {
                "title": event_info_4["title"],
                "level": topic_info_4["level"],
                "date": event_basic_info_4["date"],
                "start_time": event_basic_info_4["start_time"],
                "end_time": event_basic_info_4["end_time"],
                "event_basic_id": event_basic_4_id,
            },
        }
        self.assertEqual(rv.json["data"]["events"][0], ans_1)
        self.assertEqual(rv.json["data"]["events"][1], ans_2)
        self.assertEqual(rv.json["data"]["events"][2], ans_3)
        self.assertEqual(rv.json["data"]["events"][3], ans_4)
